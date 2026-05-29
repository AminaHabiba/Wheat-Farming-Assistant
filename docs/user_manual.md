# User Manual
## AI-Powered Wheat Farming Assistant

---

## System Requirements
- OS: Windows 10 or above
- RAM: 8 GB minimum (16 GB recommended)
- Storage: 10 GB free disk space
- Browser: Google Chrome or Microsoft Edge

---

## Installation

### Step 1: Install Python 3.10
```bash
python --version
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install Ollama
Download from https://ollama.com/download then run:
```bash
ollama pull llama3.2:3b
```

---

## Running the Application
```bash
python main.py
```
Opens browser automatically at http://localhost:8501

---

## Disease Detection
1. Click **Disease Detection** tab
2. Upload wheat leaf image (JPG or PNG)
3. Click **Analyze Wheat Leaf** button
4. Read disease result, treatment, fertilizer and farming tips

---

## AI Chatbot
1. Click **Farming Assistant** tab
2. Click a suggested question or type your own
3. Works completely offline 

---

## Stopping the Application
Press **CTRL+C** in terminal

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Backend not running | Run `python main.py` again |
| Ollama not running | Run `ollama serve` in new terminal |
| File type error | Upload JPG or PNG only |
| Image too small | Minimum 100×100 pixels |
| Browser not opening | Go to http://localhost:8501 manually |

---

## Important Notes
- Recommendations are guidance only
- Consult agricultural extension officer for severe outbreaks
- Wear protective gear when applying fungicides
- Follow 14–21 day pre-harvest interval after spraying