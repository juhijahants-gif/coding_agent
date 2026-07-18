import streamlit as st
from utils.llm import call_llm
from dotenv import load_dotenv
import time

load_dotenv()

# =========================================================
# PAGE CONFIG (must be the first Streamlit call)
# =========================================================
st.set_page_config(
    page_title="CodeMate AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# STYLING — animated background, glow orbs, glass cards
# =========================================================
st.markdown("""
<style>

/* ---------- Hide default Streamlit chrome ---------- */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ---------- Animated Gradient Background ---------- */
.stApp {
    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #0f2027);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* ---------- Floating Glow Orbs ---------- */
.glow {
    position: fixed;
    width: 320px;
    height: 320px;
    border-radius: 50%;
    filter: blur(10px);
    z-index: 0;
    pointer-events: none;
    animation: float 11s infinite ease-in-out;
}

.glow1 {
    top: 8%;
    left: 12%;
    background: radial-gradient(circle, rgba(0,198,255,0.35), transparent 70%);
}

.glow2 {
    top: 55%;
    left: 75%;
    background: radial-gradient(circle, rgba(0,114,255,0.30), transparent 70%);
    animation-delay: 3s;
}

.glow3 {
    top: 78%;
    left: 15%;
    width: 220px;
    height: 220px;
    background: radial-gradient(circle, rgba(155,89,255,0.28), transparent 70%);
    animation-delay: 6s;
}

@keyframes float {
    0%   { transform: translateY(0px) translateX(0px); }
    50%  { transform: translateY(-45px) translateX(20px); }
    100% { transform: translateY(0px) translateX(0px); }
}

/* ---------- Title ---------- */
.title {
    font-size: 46px;
    font-weight: 800;
    background: linear-gradient(90deg, #00c6ff, #0072ff, #9b59ff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
    margin-bottom: 0px;
}

@keyframes shine {
    to { background-position: 200% center; }
}

.subtitle {
    color: rgba(255,255,255,0.65);
    font-size: 16px;
    margin-top: -8px;
    margin-bottom: 25px;
}

/* ---------- Glass Card ---------- */
.card {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    margin-bottom: 14px;
    color: #eaeaea;
    position: relative;
    z-index: 1;
}

.card:hover {
    border: 1px solid rgba(0,198,255,0.4);
    box-shadow: 0 0 25px rgba(0,198,255,0.15);
    transition: all 0.3s ease-in-out;
}

/* ---------- Sidebar Glass ---------- */
section[data-testid="stSidebar"] {
    background: rgba(15, 32, 39, 0.95);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* ---------- Text visibility fixes (labels, captions, headings) ---------- */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

p, span, label, .stMarkdown, .stCaption, div[data-testid="stCaptionContainer"] {
    color: #f1f1f1 !important;
}

/* Don't let the global text-color rule wash out syntax highlighting */
pre, code, pre *, code * {
    color: initial !important;
}

/* ---------- Code blocks (st.code) ---------- */
div[data-testid="stCodeBlock"] {
    background-color: #0d1117 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

div[data-testid="stCodeBlock"] pre {
    background-color: #0d1117 !important;
}

div[data-testid="stCodeBlock"] code {
    color: #e6edf3 !important;
}

/* Typewriter streaming preview box */
.card pre {
    color: #eaeaea !important;
    background: transparent !important;
    white-space: pre-wrap !important;
}

/* Sidebar specific text */
section[data-testid="stSidebar"] * {
    color: #f5f5f5 !important;
}

section[data-testid="stSidebar"] h1 {
    color: #ffffff !important;
    font-weight: 700;
}

/* Widget labels (Model, Mode, Creativity, text_area label, etc.) */
div[data-testid="stWidgetLabel"] label,
div[data-testid="stWidgetLabel"] p {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Radio button options */
div[role="radiogroup"] label,
div[role="radiogroup"] p {
    color: #f1f1f1 !important;
}

/* Selectbox selected value + dropdown options */
div[data-baseweb="select"] * {
    color: #111111 !important;
}

/* Slider value text */
div[data-testid="stSlider"] label,
div[data-testid="stSlider"] div {
    color: #ffffff !important;
}

/* Sidebar caption / footer note */
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] small {
    color: #cfcfcf !important;
}

/* ---------- Buttons ---------- */
.stButton>button {
    border-radius: 10px;
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    color: white;
    border: none;
    font-weight: 600;
    padding: 0.6em 1.2em;
    box-shadow: 0 4px 15px rgba(0,114,255,0.35);
    transition: all 0.25s ease-in-out;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,198,255,0.55);
}

/* ---------- Text Area / Inputs ---------- */
textarea, .stTextArea textarea,
input[type="text"], input[type="number"] {
    background-color: #1b2a33 !important;
    color: #ffffff !important;
    caret-color: #ffffff !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

textarea::placeholder {
    color: rgba(255,255,255,0.45) !important;
}

/* Text selection highlight stays legible */
textarea::selection {
    background: #0072ff !important;
    color: #ffffff !important;
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.06);
    border-radius: 10px 10px 0 0;
    padding: 8px 18px;
    color: #cfcfcf;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    color: white !important;
}

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00c6ff, #0072ff);
    border-radius: 10px;
}

</style>

<!-- Floating glow orbs -->
<div class="glow glow1"></div>
<div class="glow glow2"></div>
<div class="glow glow3"></div>

""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown('<div class="title">⚡ CodeMate AI <div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Generate • Explain • Debug code like a pro 🚀</div>', unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("⚙️ Settings")

model = st.sidebar.selectbox(
    "Model",
    ["llama-3.1-8b-instant", "llama-3.1-70b-versatile"]
)

mode = st.sidebar.radio(
    "Mode",
    ["Code Only", "Code + Explanation"]
)

temperature = st.sidebar.slider("Creativity", 0.0, 1.0, 0.7)

st.sidebar.markdown("---")
st.sidebar.caption("Built with ❤️ using Streamlit + LLMs")

# =========================================================
# SESSION STATE INIT
# =========================================================
if "last_code" not in st.session_state:
    st.session_state["last_code"] = ""

# =========================================================
# INPUT
# =========================================================
task = st.text_area("💬 What do you want to build?", height=120, placeholder="e.g. Write a function to reverse a linked list")

col1, col2 = st.columns(2)
generate_clicked = col1.button("🚀 Generate", use_container_width=True)
debug_clicked = col2.button("🐞 Auto Debug", use_container_width=True)

# =========================================================
# GENERATE
# =========================================================
if generate_clicked:
    if task.strip():
        with st.spinner("Generating..."):
            prompt = f"""
You are a senior Python developer.

Task:
{task}

Return:
"""
            if mode == "Code Only":
                prompt += "\nONLY code. No explanation."
            else:
                prompt += "\nCode first, then explanation."

            response = call_llm(prompt, model=model)

        if response:
            clean = response.replace("```python", "").replace("```", "").strip()

            # Streaming/typewriter effect
            placeholder = st.empty()
            text = ""
            for char in clean:
                text += char
                placeholder.markdown(
                    f"<div class='card'><pre style='white-space:pre-wrap'>{text}</pre></div>",
                    unsafe_allow_html=True
                )
                time.sleep(0.001)

            # Tabs
            tab1, tab2, tab3 = st.tabs(["💻 Code", "🧠 Explanation", "🐞 Debug"])

            with tab1:
                st.code(clean, language="python")
                st.download_button("📥 Download", clean, "code.py")

            with tab2:
                if mode == "Code + Explanation":
                    st.write(clean)
                else:
                    st.info("Enable 'Code + Explanation' mode to see explanations here.")

            with tab3:
                st.info("Click '🐞 Auto Debug' below to fix and explain issues in this code.")

            st.session_state["last_code"] = clean

        else:
            st.error("❌ Failed to generate. Please check your API key / connection.")
    else:
        st.warning("Please describe what you want to build first!")

# =========================================================
# DEBUG
# =========================================================
if debug_clicked:
    code = st.session_state.get("last_code")

    if code:
        with st.spinner("Debugging..."):
            debug_prompt = f"""
Fix this Python code and explain the fix:

{code}
"""
            debug_response = call_llm(debug_prompt, model=model)

        if debug_response:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🛠 Fixed Code")
            st.code(debug_response, language="python")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Debug failed. Please try again.")
    else:
        st.warning("Generate code first!")