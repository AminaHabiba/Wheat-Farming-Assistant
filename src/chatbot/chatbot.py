# src/chatbot/chatbot.py

# Local AI Chatbot using Ollama + Llama3.2
# No internet required after setup.
# Combines Llama3.2 intelligence with local JSON knowledge base.

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()
                    .parent.parent.parent))

import json
import ollama

# ── Paths ────────────────────────────────────────────────────
REC_DIR = Path(__file__).resolve()\
          .parent.parent / "recommendation"

DISEASE_INFO_PATH  = REC_DIR / "disease_info.json"
TREATMENT_PATH     = REC_DIR / "treatment_data.json"
FARMING_TIPS_PATH  = REC_DIR / "farming_tips.json"

# ── Model Settings ───────────────────────────────────────────
MODEL_NAME     = "llama3.2:3b"
MAX_TOKENS     = 1024
TEMPERATURE    = 0.7


# ── Load Knowledge Base ──────────────────────────────────────
def load_knowledge_base():
    """
    Loads all three JSON files.
    Returns combined knowledge string
    to inject into chatbot context.
    """
    with open(str(DISEASE_INFO_PATH),
              "r", encoding="utf-8") as f:
        disease_info = json.load(f)

    with open(str(TREATMENT_PATH),
              "r", encoding="utf-8") as f:
        treatment_data = json.load(f)

    with open(str(FARMING_TIPS_PATH),
              "r", encoding="utf-8") as f:
        farming_tips = json.load(f)

    return disease_info, \
           treatment_data, \
           farming_tips


# ── Build System Prompt ──────────────────────────────────────
def build_system_prompt():
    """
    Builds the system prompt that tells
    Llama3.2 how to behave and what it knows.

    Injects your JSON knowledge so the model
    gives Pakistan-specific answers.
    """
    disease_info, treatment_data, \
        farming_tips = load_knowledge_base()

    # extract key knowledge
    diseases_summary = ""
    for disease, info in disease_info.items():
        if disease == "healthy":
            continue
        diseases_summary += f"""
{info['display_name']}:
- Description: {info['description']}
- Severity: {info['severity_label']}
- Season Risk: {info['season_risk']}
- Economic Impact: {info['economic_impact']}
- Symptoms: {', '.join(info['symptoms'][:3])}
- Causes: {', '.join(info['causes'][:3])}
"""

    # extract treatment summary
    treatment_summary = ""
    for disease, treatment in \
            treatment_data.items():
        if disease == "healthy":
            continue
        name = disease.replace("_", " ").title()
        if treatment["chemical_treatments"]:
            t = treatment[
                "chemical_treatments"][0]
            treatment_summary += f"""
{name}:
- Best fungicide: {t['name']}
- Brands available in Pakistan: {', '.join(t['brand_names'])}
- Dose: {t['dose']}
- Timing: {treatment['application_timing']}
"""

    # extract farming tips summary
    sowing     = farming_tips[
        "general_tips"]["sowing"]
    irrigation = farming_tips[
        "general_tips"]["irrigation"]
    varieties  = farming_tips[
        "variety_recommendations"][
        "rust_resistant"]

    system_prompt = f"""You are an expert AI Wheat Farming Assistant for Pakistani farmers, developed by Amina Habiba at the University of Agriculture Faisalabad (UAF).

Your role is to help wheat farmers in Pakistan — especially Punjab — with:
1. Wheat disease detection and treatment
2. Farming guidance and best practices
3. Fertilizer and irrigation recommendations
4. Variety selection and crop management

## Your Knowledge Base (Pakistan-Specific):

### Wheat Diseases You Know About:
{diseases_summary}

### Treatment & Fungicides Available in Pakistan:
{treatment_summary}

### Sowing Guidelines for Punjab Pakistan:
{chr(10).join([f'- {s}' for s in sowing[:5]])}

### Irrigation Schedule:
{chr(10).join([f'- {i}' for i in irrigation[:5]])}

### Recommended Rust-Resistant Varieties:
{chr(10).join([f'- {v}' for v in varieties])}

## How You Should Respond:
- Always give practical, actionable advice
- Use simple language farmers can understand
- Mention specific product names available in Pakistan
- Always recommend consulting local agricultural extension officer for severe cases
- Keep responses clear and well-organized
- Use bullet points and sections for clarity
- Focus on wheat farming in Pakistan context
- If asked about other crops, you can answer briefly but focus on wheat
- Always be helpful, friendly and encouraging to farmers

## Important Rules:
- Never recommend unsafe chemical doses
- Always mention safety precautions for chemicals
- Encourage farmers to seek expert help for severe outbreaks
- Provide economically practical advice for small farmers"""

    return system_prompt


# ── Check Ollama Running ─────────────────────────────────────
def check_ollama():
    try:
        models = ollama.list()

        # handle different ollama library versions
        model_list = models.get("models", [])
        model_names = []

        for m in model_list:
            # newer versions use 'model' key
            # older versions use 'name' key
            name = m.get("model", "") or \
                   m.get("name", "")
            if name:
                model_names.append(name)

        if any(MODEL_NAME in m
               for m in model_names):
            return True, "Ollama ready"
        else:
            # try direct connection test
            test = ollama.chat(
                model=MODEL_NAME,
                messages=[{
                    "role": "user",
                    "content": "hi"
                }],
                options={"num_predict": 5}
            )
            if test:
                return True, "Ollama ready"
            return False, \
                f"Model {MODEL_NAME} not found."

    except Exception as e:
        return False, \
            f"Ollama not running: {str(e)}"

# ── Chat Function ────────────────────────────────────────────
def chat(question, chat_history=None):
    """
    Main chat function.
    Sends question to Llama3.2 with
    wheat farming context.

    question     : string from farmer
    chat_history : list of previous messages
                   for multi-turn conversation

    Output : string answer from AI
    """
    if not question or \
            not question.strip():
        return "Please type your question!"

    try:
        # build messages list
        messages = []

        # system prompt with knowledge base
        system_prompt = build_system_prompt()
        messages.append({
            "role"   : "system",
            "content": system_prompt
        })

        # add chat history for context
        if chat_history:
            for msg in chat_history[-6:]:
                # last 6 messages for context
                messages.append({
                    "role"   : msg["role"],
                    "content": msg["content"]
                })

        # add current question
        messages.append({
            "role"   : "user",
            "content": question
        })

        # call Ollama
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            options={
                "temperature": TEMPERATURE,
                "num_predict": MAX_TOKENS
            }
        )

        return response["message"]["content"]

    except Exception as e:
        return f"""❌ Chatbot Error: {str(e)}

**Possible solutions:**
1. Make sure Ollama is running
2. Open new terminal and run: `ollama serve`
3. Then restart the Streamlit app"""


# ── Stream Chat Function ─────────────────────────────────────
def chat_stream(question, chat_history=None):
    """
    Streaming version of chat.
    Yields response word by word.
    Used for typing effect in Streamlit.

    question     : string from farmer
    chat_history : list of previous messages

    Output : generator yielding text chunks
    """
    if not question or \
            not question.strip():
        yield "Please type your question!"
        return

    try:
        system_prompt = build_system_prompt()
        messages      = []

        messages.append({
            "role"   : "system",
            "content": system_prompt
        })

        if chat_history:
            for msg in chat_history[-6:]:
                messages.append({
                    "role"   : msg["role"],
                    "content": msg["content"]
                })

        messages.append({
            "role"   : "user",
            "content": question
        })

        # stream response
        stream = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            stream=True,
            options={
                "temperature": TEMPERATURE,
                "num_predict": MAX_TOKENS
            }
        )

        for chunk in stream:
            content = chunk[
                "message"]["content"]
            if content:
                yield content

    except Exception as e:
        yield f"❌ Error: {str(e)}"


# ── Quick Test ───────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  Wheat Chatbot — Ollama Test")
    print("=" * 55)

    # check ollama
    ok, msg = check_ollama()
    if not ok:
        print(f"❌ {msg}")
        sys.exit(1)

    print(f"✅ {msg}")
    print(f"   Model: {MODEL_NAME}\n")

    # test questions
    test_questions = [
        "What is stripe rust?",
        "Which fungicide should I use "
        "for leaf rust in Pakistan?",
        "When should I irrigate my wheat?",
        "What fertilizer is best for wheat?",
        "How can I prevent powdery mildew?"
    ]

    for q in test_questions:
        print(f"\n👨‍🌾 Farmer: {q}")
        print("-" * 45)
        response = chat(q)
        # show first 5 lines
        lines = response.split("\n")[:6]
        print("\n".join(lines))
        if len(response.split("\n")) > 6:
            print("...")

    print("\n" + "=" * 55)
    print("Chatbot test complete!")
    print("=" * 55)