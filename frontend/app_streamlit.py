# frontend/app_streamlit.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve()
                    .parent.parent))

import streamlit as st
import requests
from PIL import Image
import base64

# Page Config
st.set_page_config(
    page_title="Wheat Farming Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paths
ASSETS_DIR = Path(__file__).resolve().parent \
             / "assets"
UAF_LOGO   = ASSETS_DIR / "uaf_logo.png"

# Constants
API_URL = "http://localhost:5000"

DISEASE_COLORS = {
    "healthy"       : "#2E7D32",
    "leaf_rust"     : "#C62828",
    "stripe_rust"   : "#E65100",
    "powdery_mildew": "#6A1B9A"
}

DISEASE_ICONS = {
    "healthy"       : "✅",
    "leaf_rust"     : "🔴",
    "stripe_rust"   : "🟡",
    "powdery_mildew": "⚪"
}

SEVERITY_COLORS = {
    "none"     : "#2E7D32",
    "medium"   : "#F57F17",
    "high"     : "#C62828",
    "very_high": "#B71C1C"
}

SEVERITY_ICONS = {
    "none"     : "✅",
    "medium"   : "⚠️",
    "high"     : "🔴",
    "very_high": "🚨"
}


# Load Image As Base64
def get_image_base64(image_path):
    try:
        with open(str(image_path), "rb") as f:
            return base64.b64encode(
                f.read()).decode("utf-8")
    except Exception:
        return None


# Custom CSS
def load_css():
    st.markdown("""
    <style>
        .block-container {
            padding-top: 4rem !important;
        }
        .main-header {
            background: linear-gradient(
                135deg,
                #1B5E20 0%,
                #2E7D32 50%,
                #1B5E20 100%
            );
            padding: 25px 35px;
            border-radius: 16px;
            color: white;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px
                        rgba(27,94,32,0.3);
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .main-header h1 {
            font-size: 1.9rem;
            margin: 0;
            font-weight: 800;
            color: white;
        }
        .main-header p {
            font-size: 0.9rem;
            margin: 5px 0 0 0;
            opacity: 0.9;
        }

        /* White circular badge behind the original UAF logo */
        .main-header-logo-circle {
            width: 100px;
            height: 100px;
            min-width: 100px;
            border-radius: 50%;
            background-color: #ffffff;
            border: 3px solid
                        rgba(255,255,255,0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            box-sizing: border-box;
        }
        /* The logo itself stays transparent and keeps its original shape */
        .main-header-logo {
            width: 75px;
            height: 75px;
            object-fit: contain;
            display: block;
            background: transparent;
            padding: 0;
            border: none;
            border-radius: 0;
        }

        .healthy-card {
            background: linear-gradient(
                135deg, #e8f5e9, #f1f8e9);
            border-radius: 14px;
            padding: 20px 25px;
            margin: 10px 0;
            border-left: 6px solid #2E7D32;
            box-shadow: 0 3px 12px
                        rgba(46,125,50,0.15);
        }
        .disease-card {
            background: linear-gradient(
                135deg, #fff8e1, #fff3e0);
            border-radius: 14px;
            padding: 20px 25px;
            margin: 10px 0;
            border-left: 6px solid #E65100;
            box-shadow: 0 3px 12px
                        rgba(230,81,0,0.15);
        }
        .urgent-card {
            background: linear-gradient(
                135deg, #ffebee, #fce4ec);
            border-radius: 14px;
            padding: 20px 25px;
            margin: 10px 0;
            border-left: 6px solid #C62828;
            box-shadow: 0 3px 12px
                        rgba(198,40,40,0.15);
        }
        .metric-row {
            display: flex;
            gap: 12px;
            margin: 15px 0;
        }
        .metric-card {
            flex: 1;
            background: white;
            border-radius: 12px;
            padding: 14px;
            text-align: center;
            box-shadow: 0 2px 8px
                        rgba(0,0,0,0.08);
            border-top: 4px solid #2E7D32;
        }
        .metric-card .metric-value {
            font-size: 1.4rem;
            font-weight: 800;
            color: #1B5E20;
        }
        .metric-card .metric-label {
            font-size: 0.78rem;
            color: #666;
            margin-top: 4px;
        }
        .severity-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            color: white;
            margin-left: 8px;
        }
        .section-header {
            font-size: 1rem;
            font-weight: 700;
            color: #1B5E20;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 5px;
            margin: 15px 0 10px 0;
        }
        .info-box {
            background: #e3f2fd;
            border-radius: 10px;
            padding: 10px 14px;
            margin: 7px 0;
            border-left: 4px solid #1565C0;
            font-size: 0.9rem;
        }
        .warning-box {
            background: #fff3e0;
            border-radius: 10px;
            padding: 10px 14px;
            margin: 7px 0;
            border-left: 4px solid #E65100;
            font-size: 0.9rem;
        }
        .prob-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 7px 0;
        }
        .prob-label {
            width: 140px;
            font-size: 0.87rem;
            font-weight: 500;
        }
        .prob-bar-bg {
            flex: 1;
            background: #f0f0f0;
            border-radius: 10px;
            height: 18px;
            overflow: hidden;
        }
        .prob-bar-fill {
            height: 100%;
            border-radius: 10px;
        }
        .prob-value {
            width: 52px;
            text-align: right;
            font-size: 0.87rem;
            font-weight: 700;
        }

        /* Chatbot Styles */
        .chat-container {
            background: #f8f9fa;
            border-radius: 14px;
            padding: 20px;
            margin: 10px 0;
            min-height: 400px;
            max-height: 500px;
            overflow-y: auto;
            border: 1px solid #e0e0e0;
        }
        .chat-message-user {
            display: flex;
            justify-content: flex-end;
            margin: 10px 0;
        }
        .chat-message-bot {
            display: flex;
            justify-content: flex-start;
            margin: 10px 0;
        }
        .chat-bubble-user {
            background: #1B5E20;
            color: white;
            padding: 10px 16px;
            border-radius: 18px 18px 4px 18px;
            max-width: 70%;
            font-size: 0.92rem;
        }
        .chat-bubble-bot {
            background: white;
            color: #333;
            padding: 10px 16px;
            border-radius: 18px 18px 18px 4px;
            max-width: 75%;
            font-size: 0.92rem;
            border: 1px solid #e0e0e0;
            box-shadow: 0 1px 4px
                        rgba(0,0,0,0.08);
        }
        .chat-avatar-user {
            width: 32px;
            height: 32px;
            background: #1B5E20;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.85rem;
            margin-left: 8px;
            flex-shrink: 0;
        }
        .chat-avatar-bot {
            width: 32px;
            height: 32px;
            background: #4CAF50;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.85rem;
            margin-right: 8px;
            flex-shrink: 0;
        }
        .chat-welcome {
            text-align: center;
            padding: 30px 20px;
            color: #666;
        }
        .chat-welcome h3 {
            color: #1B5E20;
            font-size: 1.2rem;
        }
        .suggested-question {
            display: inline-block;
            background: #e8f5e9;
            color: #1B5E20;
            border: 1px solid #4CAF50;
            border-radius: 20px;
            padding: 6px 14px;
            margin: 4px;
            font-size: 0.83rem;
            cursor: pointer;
            font-weight: 500;
        }
        .dev-card {
            background: linear-gradient(
                135deg, #1B5E20, #2E7D32);
            border-radius: 12px;
            padding: 15px;
            color: white;
            text-align: center;
            margin-top: 10px;
        }
        .dev-card h4 {
            margin: 0 0 4px 0;
            font-size: 0.95rem;
            color: white;
        }
        .dev-card p {
            margin: 2px 0;
            font-size: 0.8rem;
            opacity: 0.9;
        }

        /* Separate white circle for the developer-card logo too */
        .dev-logo-circle {
            width: 48px;
            height: 48px;
            margin: 0 auto 6px auto;
            border-radius: 50%;
            background: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        .dev-logo {
            width: 42px;
            height: 42px;
            object-fit: contain;
            display: block;
            background: transparent;
            padding: 0;
            border: none;
            border-radius: 0;
        }

        .footer {
            background: linear-gradient(
                135deg, #1B5E20, #2E7D32);
            color: white;
            text-align: center;
            font-size: 0.83rem;
            margin-top: 30px;
            padding: 18px;
            border-radius: 12px;
        }
        .step-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin: 10px 0;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 8px;
        }
        .step-icon {
            font-size: 1.3rem;
            flex-shrink: 0;
        }
    </style>
    """, unsafe_allow_html=True)


# Check API
def check_api():
    try:
        r = requests.get(
            f"{API_URL}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


# Check Ollama
def check_ollama():
    try:
        import ollama
        ollama.list()
        return True
    except Exception:
        return False


# Call Predict API
def call_predict_api(image_bytes, filename):
    try:
        files = {"image": (
            filename, image_bytes,
            "image/jpeg")}
        response = requests.post(
            f"{API_URL}/predict",
            files=files, timeout=30)
        return response.json()
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": "Cannot connect to backend."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# Call Chatbot
def call_chatbot(question, chat_history):
    """
    Calls local Ollama chatbot.
    Returns response string.
    """
    try:
        from src.chatbot.chatbot import chat
        response = chat(question, chat_history)
        return response
    except Exception as e:
        return f"❌ Chatbot error: {str(e)}\n\n" \
               f"Make sure Ollama is running:\n" \
               f"`ollama serve`"


# Probability Bars
def show_probability_bars(all_probs, disease):
    bars_html = ""
    for cls, prob in all_probs.items():
        label = cls.replace("_", " ").title()
        color = DISEASE_COLORS.get(cls, "#666")
        icon = DISEASE_ICONS.get(cls, "•")
        bold = "font-weight:800;" \
            if cls == disease else ""

        bars_html += f"""
        <div class="prob-row">
            <div class="prob-label"
                 style="{bold}">
                {icon} {label}
            </div>
            <div class="prob-bar-bg">
                <div class="prob-bar-fill"
                     style="width:{prob}%;
                     background:{color};">
                </div>
            </div>
            <div class="prob-value"
                 style="color:{color};{bold}">
                {prob}%
            </div>
        </div>"""

    st.markdown(bars_html,
                unsafe_allow_html=True)


# Sidebar
def show_sidebar():
    with st.sidebar:

        # UAF Logo
        if UAF_LOGO.exists():
            sidebar_logo_b64 = get_image_base64(UAF_LOGO)
            st.markdown(
                f"""
                <div style='display:flex;
                align-items:center;gap:10px;
                padding:6px 0'>
                    <img src="data:image/png;base64,{sidebar_logo_b64}"
                    width="70"
                    style="flex-shrink:0">
                    <div style='line-height:1.3'>
                    <b style='font-size:0.91rem;
                    color:#1B5E20'>
                    University of Agriculture
                    </b><br>
                    <span style='font-size:0.90rem;
                    color:#666'>
                    Faisalabad
                    </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style='text-align:center;
                background:#1B5E20;color:white;
                padding:10px;border-radius:8px;
                font-weight:700'>
                🎓 UAF Faisalabad
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown(
            """
            <div style='font-size:0.88rem'>
            <b>🌾 About</b><br><br>
            AI-powered assistant for Pakistani
            farmers to detect wheat diseases
            and get instant recommendations.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")
        st.markdown("**📊 Model Performance**")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Val Acc", "93.55%",
                      delta="+1.57%")
        with c2:
            st.metric("Test Acc", "92.69%",
                      delta="+2.02%")

        st.markdown("---")
        st.markdown("**🦠 Detectable Diseases**")
        diseases = [
            ("✅ Healthy", "#2E7D32"),
            ("🔴 Leaf Rust", "#C62828"),
            ("🟡 Stripe Rust", "#E65100"),
            ("⚪ Powdery Mildew", "#6A1B9A")
        ]
        for label, color in diseases:
            st.markdown(
                f"<div style='padding:5px 10px;"
                f"margin:3px 0;"
                f"background:{color}15;"
                f"border-left:3px solid {color};"
                f"border-radius:6px;"
                f"font-size:0.86rem;"
                f"font-weight:600;"
                f"color:{color}'>"
                f"{label}</div>",
                unsafe_allow_html=True
            )

        st.markdown("---")

        # Service Status
        st.markdown("**🔌 Service Status**")
        api_ok = check_api()
        ollama_ok = check_ollama()

        statuses = [
            ("Flask Backend", api_ok,
             "python backend/app.py"),
            ("Ollama AI", ollama_ok,
             "ollama serve")
        ]

        for name, ok, cmd in statuses:
            if ok:
                st.markdown(
                    f"<div style='background:"
                    f"#e8f5e9;padding:6px 10px;"
                    f"border-radius:7px;"
                    f"border-left:3px solid "
                    f"#2E7D32;font-size:0.83rem;"
                    f"font-weight:600;"
                    f"color:#2E7D32;margin:3px 0'>"
                    f"🟢 {name}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='background:"
                    f"#ffebee;padding:6px 10px;"
                    f"border-radius:7px;"
                    f"border-left:3px solid "
                    f"#C62828;font-size:0.83rem;"
                    f"font-weight:600;"
                    f"color:#C62828;margin:3px 0'>"
                    f"🔴 {name}: `{cmd}`</div>",
                    unsafe_allow_html=True
                )

        st.markdown("---")

        # Developer Card
        logo_b64 = get_image_base64(UAF_LOGO) \
            if UAF_LOGO.exists() else None
        logo_img = (
            f'<div class="dev-logo-circle">'
            f'<img src="data:image/png;base64,'
            f'{logo_b64}" class="dev-logo">'
            f'</div>'
            if logo_b64
            else '👩‍💻'
        )
        st.markdown(
            f"""
            <div class="dev-card">
                {logo_img}
                <h4>Amina Habiba</h4>
                <p>BS Computer Science</p>
                <p>Batch 2022-2026</p>
                <p>UAF Faisalabad - 2026</p>
                <p style='margin-top:6px;
                font-size:0.73rem;opacity:0.8'>
                Supervised by:<br>
                Dr. Ahsan Latif
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# Show Prediction
def show_prediction(result):
    pred = result["prediction"]
    rec = result["recommendation"]
    info = rec["disease_info"]
    disease = pred["disease"]

    confidence = pred["confidence"]
    is_healthy = pred["is_healthy"]
    is_uncertain = pred["is_uncertain"]
    severity = info["severity"]

    color = DISEASE_COLORS.get(
        disease, "#666")
    icon = DISEASE_ICONS.get(
        disease, "•")
    sev_color = SEVERITY_COLORS.get(
        severity, "#666")
    sev_icon = SEVERITY_ICONS.get(
        severity, "•")

    card_class = "healthy-card" \
        if is_healthy \
        else "urgent-card" \
        if severity == "very_high" \
        else "disease-card"

    st.markdown(
        f"""
        <div class="{card_class}">
            <div style='display:flex;
            align-items:center;gap:12px'>
                <span style='font-size:2.2rem'>
                    {icon}
                </span>
                <div>
                    <h2 style='color:{color};
                    margin:0;font-size:1.6rem'>
                        {info['display_name']}
                        <span class="severity-badge"
                        style="background:{sev_color}">
                            {sev_icon}
                            {info['severity_label']
                             .split('—')[0].strip()}
                        </span>
                    </h2>
                    <p style='margin:5px 0 0 0;
                    font-size:0.95rem;color:#444'>
                        {pred['message']}
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if is_uncertain:
        st.warning(
            "⚠️ Low confidence - please upload "
            "a clearer image."
        )

    # Metrics
    st.markdown(
        f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="metric-value"
                style="color:{color}">
                    {icon} {info['display_name']}
                </div>
                <div class="metric-label">
                    Detected Disease
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-value"
                style="color:{color}">
                    {confidence}%
                </div>
                <div class="metric-label">
                    Confidence
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-value"
                style="color:{sev_color}">
                    {sev_icon}
                    {info['severity']
                    .replace('_',' ').title()}
                </div>
                <div class="metric-label">
                    Severity
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-value"
                style="color:#1565C0;
                font-size:0.9rem">
                    {info['economic_impact']
                    .split('if')[0].strip()}
                </div>
                <div class="metric-label">
                    Economic Impact
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Probability bars
    st.markdown(
        "<div class='section-header'>"
        "📊 Prediction Probabilities</div>",
        unsafe_allow_html=True
    )
    show_probability_bars(
        pred["all_probs"], disease)

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Disease Info",
        "💊 Treatment",
        "🌱 Fertilizer",
        "🌾 Farming Tips"
    ])

    with tab1:
        st.markdown(
            f"<div class='info-box'>"
            f"📝 {info['description']}</div>",
            unsafe_allow_html=True
        )
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "<div class='section-header'>"
                "🔍 Symptoms</div>",
                unsafe_allow_html=True
            )
            for s in info["symptoms"]:
                st.markdown(f"• {s}")
        with col2:
            st.markdown(
                "<div class='section-header'>"
                "⚗️ Causes</div>",
                unsafe_allow_html=True
            )
            for c in info["causes"]:
                st.markdown(f"• {c}")

        if info["affected_parts"]:
            st.markdown(
                f"<div class='info-box'>"
                f"🌿 <b>Affected Parts:</b> "
                f"{' | '.join(info['affected_parts'])}"
                f"</div>",
                unsafe_allow_html=True
            )
        st.markdown(
            f"<div class='warning-box'>"
            f"📅 <b>Season Risk:</b> "
            f"{info['season_risk']}</div>",
            unsafe_allow_html=True
        )

    with tab2:
        treatment = rec["treatment"]
        st.markdown(
            "<div class='section-header'>"
            "⚡ Immediate Actions</div>",
            unsafe_allow_html=True
        )
        for i, a in enumerate(
                treatment["immediate_actions"]):
            st.markdown(
                f"<div style='background:#fff8e1;"
                f"padding:7px 12px;margin:4px 0;"
                f"border-radius:7px;"
                f"border-left:3px solid {color};"
                f"font-size:0.88rem'>"
                f"{i+1}. {a}</div>",
                unsafe_allow_html=True
            )

        if treatment["chemical_treatments"]:
            st.markdown(
                "<div class='section-header'>"
                "💊 Chemical Treatments</div>",
                unsafe_allow_html=True
            )
            for t in \
                    treatment["chemical_treatments"]:
                with st.expander(
                    f"🧪 {t['name']} — "
                    f"{t['effectiveness']}"
                ):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(
                            f"**💊 Dose:** {t['dose']}")
                        st.write(
                            f"**🔄 Frequency:** "
                            f"{t['frequency']}")
                    with c2:
                        st.write(
                            f"**🏷️ Brands:** "
                            f"{', '.join(t['brand_names'])}")
                        st.write(
                            f"**📋 Method:** "
                            f"{t['method']}")
                    st.markdown(
                        f"<div class='info-box'>"
                        f"📝 {t['notes']}</div>",
                        unsafe_allow_html=True
                    )

        st.markdown(
            "<div class='section-header'>"
            "🌿 Biological Treatments</div>",
            unsafe_allow_html=True
        )
        for bio in \
                treatment["biological_treatments"]:
            st.markdown(f"• {bio}")

        st.markdown(
            "<div class='section-header'>"
            "🛡️ Preventive Measures</div>",
            unsafe_allow_html=True
        )
        for prev in \
                treatment["preventive_measures"]:
            st.markdown(f"• {prev}")

        st.markdown(
            f"<div class='warning-box'>"
            f"⏰ <b>Timing:</b> "
            f"{treatment['application_timing']}"
            f"</div>",
            unsafe_allow_html=True
        )

        if treatment["safety_precautions"]:
            st.markdown(
                "<div class='section-header'>"
                "⚠️ Safety</div>",
                unsafe_allow_html=True
            )
            for s in \
                    treatment["safety_precautions"]:
                st.markdown(
                    f"<span style='color:#E65100'>"
                    f"⚠️</span> {s}",
                    unsafe_allow_html=True)

    with tab3:
        fertilizer = rec["fertilizer"]
        st.markdown(
            f"<div class='warning-box'>"
            f"📝 <b>Note:</b> "
            f"{fertilizer['special_notes']}"
            f"</div>",
            unsafe_allow_html=True
        )
        c1, c2, c3 = st.columns(3)
        fert_data = [
            (c1, "🟡 Nitrogen",
             fertilizer["nitrogen"], "#F9A825"),
            (c2, "🔵 Phosphorus",
             fertilizer["phosphorus"], "#1565C0"),
            (c3, "🟤 Potassium",
             fertilizer["potassium"], "#4E342E")
        ]
        for col, title, data, fc in fert_data:
            with col:
                st.markdown(
                    f"<div style='background:"
                    f"white;border-radius:10px;"
                    f"padding:14px;border-top:"
                    f"4px solid {fc};"
                    f"box-shadow:0 2px 6px "
                    f"rgba(0,0,0,0.07)'>"
                    f"<b style='color:{fc}'>"
                    f"{title}</b><br>"
                    f"<span style='font-size:"
                    f"0.83rem'>"
                    f"{data['total_dose']}"
                    f"</span></div>",
                    unsafe_allow_html=True
                )
                for s in data["schedule"]:
                    st.markdown(
                        f"<div style='font-size:"
                        f"0.83rem'>• {s}</div>",
                        unsafe_allow_html=True
                    )

        st.markdown(
            "<div class='section-header'>"
            "⚗️ Micronutrients</div>",
            unsafe_allow_html=True
        )
        for m in fertilizer["micronutrients"]:
            st.markdown(f"• {m}")

    with tab4:
        farming = rec["farming"]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                "<div class='section-header'>"
                "💧 Irrigation</div>",
                unsafe_allow_html=True
            )
            for tip in farming["irrigation"]:
                st.markdown(
                    f"<div style='font-size:"
                    f"0.86rem'>💧 {tip}</div>",
                    unsafe_allow_html=True
                )
            st.markdown(
                "<div class='section-header'>"
                "🌾 Varieties</div>",
                unsafe_allow_html=True
            )
            for v in farming["varieties"]:
                st.markdown(
                    f"<div style='color:#2E7D32;"
                    f"font-size:0.86rem'>"
                    f"🌱 {v}</div>",
                    unsafe_allow_html=True
                )
        with c2:
            st.markdown(
                "<div class='section-header'>"
                "🌱 Sowing</div>",
                unsafe_allow_html=True
            )
            for tip in farming["sowing"]:
                st.markdown(
                    f"<div style='font-size:"
                    f"0.86rem'>🌱 {tip}</div>",
                    unsafe_allow_html=True
                )
            st.markdown(
                "<div class='section-header'>"
                "🚜 Harvesting</div>",
                unsafe_allow_html=True
            )
            for tip in farming["harvesting"]:
                st.markdown(
                    f"<div style='font-size:"
                    f"0.86rem'>🚜 {tip}</div>",
                    unsafe_allow_html=True
                )


# Chatbot Tab
def show_chatbot():
    """Renders the AI chatbot interface."""

    # initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "messages_display" not in \
            st.session_state:
        st.session_state.messages_display = []

    # chatbot header
    st.markdown(
        """
        <div style='background:linear-gradient(
        135deg,#1B5E20,#2E7D32);
        padding:18px 25px;border-radius:12px;
        color:white;margin-bottom:15px'>
            <h3 style='margin:0;font-size:1.3rem;color:white'>
                🤖 AI Wheat Farming Assistant
            </h3>
            <p style='margin:5px 0 0 0;
            font-size:0.88rem;opacity:0.9'>
                Powered by Llama 3.2 - Ask anything
                about wheat farming!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # check ollama
    if not check_ollama():
        st.error(
            "❌ Ollama is not running!"
        )
        st.markdown(
            """
            **To start Ollama:**
            1. Open a new terminal
            2. Run: `ollama serve`
            3. Come back and refresh
            """
        )
        return

    # suggested questions
    st.markdown(
        "<div class='section-header'>"
        "💡 Suggested Questions</div>",
        unsafe_allow_html=True
    )

    suggested = [
        "What is leaf rust?",
        "How to treat stripe rust?",
        "When should I irrigate?",
        "Best fertilizer for wheat?",
        "How to prevent powdery mildew?",
        "Which wheat variety is best?",
        "When to sow wheat in Punjab?",
        "What causes yellow rust?"
    ]

    # show suggested questions as buttons
    cols = st.columns(4)
    for i, q in enumerate(suggested):
        with cols[i % 4]:
            if st.button(
                q,
                key=f"suggested_{i}",
                use_container_width=True
            ):
                st.session_state[
                    "pending_question"] = q

    st.markdown("---")

    # chat history display
    if not st.session_state.messages_display:
        st.markdown(
            """
            <div class='chat-welcome'>
                <h3>🌾 Hello! I'm your Wheat
                Farming Assistant</h3>
                <p>Ask me anything about wheat
                diseases, treatment, fertilizer,
                irrigation or farming practices.
                </p>
                <p style='font-size:0.85rem;
                color:#888'>
                    I provide Pakistan-specific
                    advice for Punjab farmers.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # show chat messages
        for msg in \
                st.session_state.messages_display:
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div class="chat-message-user">
                        <div class="chat-bubble-user">
                            {msg['content']}
                        </div>
                        <div class="chat-avatar-user">
                            👨‍🌾
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="chat-message-bot">
                        <div class="chat-avatar-bot">
                            🤖
                        </div>
                        <div class="chat-bubble-bot">
                            {msg['content']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("---")

    # chat input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Ask a question",
            placeholder="e.g. What is stripe "
                        "rust? How to treat "
                        "leaf rust?",
            label_visibility="collapsed",
            key="chat_input"
        )
    with col2:
        send_clicked = st.button(
            "Send 📤",
            use_container_width=True,
            type="primary"
        )

    # handle pending question from
    # suggested buttons
    if "pending_question" in \
            st.session_state:
        question = st.session_state[
            "pending_question"]
        del st.session_state["pending_question"]
        process_chat(question)

    # handle typed question
    elif send_clicked and user_input.strip():
        process_chat(user_input.strip())

    # clear chat button
    if st.session_state.messages_display:
        if st.button(
            "🗑️ Clear Chat",
            use_container_width=False
        ):
            st.session_state.chat_history = []
            st.session_state.messages_display = []
            st.rerun()


# Process Chat Message
def process_chat(question):
    """
    Processes a chat message and
    gets response from chatbot.
    """
    # add user message to display
    st.session_state.messages_display.append({
        "role": "user",
        "content": question
    })

    # add to history for context
    st.session_state.chat_history.append({
        "role": "user",
        "content": question
    })

    # get response
    with st.spinner("🤖 Thinking..."):
        response = call_chatbot(
            question,
            st.session_state.chat_history
        )

    # add bot response to display
    st.session_state.messages_display.append({
        "role": "assistant",
        "content": response
    })

    # add to history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })

    # keep history to last 10 messages
    if len(st.session_state.chat_history) > 10:
        st.session_state.chat_history = \
            st.session_state.chat_history[-10:]

    st.rerun()


# Main App
def main():
    load_css()
    show_sidebar()

    # Header
    logo_b64 = get_image_base64(UAF_LOGO) \
        if UAF_LOGO.exists() else None
    logo_html = (
        f'<div class="main-header-logo-circle">'
        f'<img src="data:image/png;base64,'
        f'{logo_b64}" class="main-header-logo">'
        f'</div>'
        if logo_b64
        else '<span style="font-size:2.5rem">'
             '🌾</span>'
    )

    st.markdown(
        f"""
        <div class="main-header">
            {logo_html}
            <div>
                <h1>🌾 AI-Powered Wheat Farming
                Assistant</h1>
                <p>Detect wheat diseases from
                leaf images & get AI-powered
                farming advice |
                University of Agriculture,
                Faisalabad</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Main tabs
    tab_detect, tab_chat = st.tabs([
        "🔍 Disease Detection",
        "💬 Farming Assistant (AI Chatbot)"
    ])

    # Tab 1: Disease Detection
    with tab_detect:

        if not check_api():
            st.error(
                "❌ Flask backend not running!"
            )
            st.code("python backend/app.py")
            st.stop()

        col1, col2 = st.columns([1.1, 0.9])

        with col1:
            st.markdown(
                "<div class='section-header'>"
                "📸 Upload Wheat Leaf Image"
                "</div>",
                unsafe_allow_html=True
            )
            uploaded_file = st.file_uploader(
                "Choose image",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed"
            )

            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(
                    image,
                    caption=f"📸 "
                            f"{uploaded_file.name}",
                    use_column_width=True
                )
                st.markdown(
                    f"<div class='info-box'>"
                    f"📁 {uploaded_file.name}"
                    f" &nbsp;|&nbsp; "
                    f"📐 {image.width}×"
                    f"{image.height}px"
                    f" &nbsp;|&nbsp; "
                    f"💾 {uploaded_file.size/1024:.1f} KB</div>",
                    unsafe_allow_html=True
                )

        with col2:
            st.markdown(
                "<div class='section-header'>"
                "📋 How To Use</div>",
                unsafe_allow_html=True
            )
            steps = [
                ("📸", "Take clear photo of "
                       "wheat leaf"),
                ("📤", "Upload image using "
                       "button on left"),
                ("🔍", "Click Analyze to "
                       "detect disease"),
                ("📋", "Get treatment and "
                       "farming advice")
            ]
            for icon, desc in steps:
                st.markdown(
                    f"""
                    <div class="step-item">
                        <span class="step-icon">
                            {icon}
                        </span>
                        <span style='font-size:
                        0.88rem'>{desc}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                """
                <div class='warning-box'
                style='margin-top:12px'>
                    💡 <b>Tips:</b> Good lighting
                    · Focus on leaf · Avoid blur
                    · Min 100×100px
                </div>
                """,
                unsafe_allow_html=True
            )

        if uploaded_file:
            st.markdown("")
            if st.button(
                "🔍 Analyze Wheat Leaf",
                type="primary",
                use_container_width=True
            ):
                with st.spinner(
                    "🔄 Analyzing image..."
                ):
                    uploaded_file.seek(0)
                    image_bytes = uploaded_file.read()
                    result = call_predict_api(
                        image_bytes,
                        uploaded_file.name
                    )

                if result["status"] == "success":
                    st.markdown("---")
                    st.markdown(
                        "<div class='section-header'>"
                        "📊 Analysis Results"
                        "</div>",
                        unsafe_allow_html=True
                    )
                    show_prediction(result)
                else:
                    st.error(
                        f"❌ {result['message']}"
                    )

    # Tab 2: Chatbot
    with tab_chat:
        show_chatbot()

    # Footer
    st.markdown(
        """
        <div class="footer">
            🌾 AI-Powered Wheat Farming Assistant
            &nbsp;|&nbsp;
            👩‍💻 Amina Habiba (2022-ag-7802)
            &nbsp;|&nbsp;
            BS Computer Science
            &nbsp;|&nbsp;
            UAF Faisalabad, 2026
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
