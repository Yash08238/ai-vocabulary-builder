import os
from dotenv import load_dotenv

# Load local .env file (optional, for local development only)
load_dotenv()

import streamlit as st

# Try to import the Google Generative AI SDK; handle gracefully if it's missing
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ModuleNotFoundError:
    genai = None
    HAS_GENAI = False

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Personal Vocabulary Builder",
    page_icon="🗣️",
    layout="wide",
)

# 🔐 Gemini API key — loaded from Streamlit secrets or environment variable
GEMINI_API_KEY = None

# Prefer Streamlit secrets when running on Streamlit Cloud
try:
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
except Exception:
    GEMINI_API_KEY = None

# Fallback to environment variable (useful for local development)
if not GEMINI_API_KEY:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validate setup and initialize the model only if SDK is available
if not GEMINI_API_KEY or GEMINI_API_KEY.strip() == "" or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
    st.error("❌ Gemini API key is missing. On Streamlit Cloud, add 'GEMINI_API_KEY' under Settings → Secrets. Locally, set environment variable 'GEMINI_API_KEY'.")
    model = None
else:
    if not HAS_GENAI:
        st.error("❌ The 'google-generative-ai' package is not installed. Add it to `requirements.txt` or install it locally (`pip install google-generative-ai`). See DEPLOYMENT.md troubleshooting.")
        model = None
    else:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-2.5-flash")
        except Exception as e:
            st.error(f"Error initializing Gemini model: {e}")
            model = None

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.header("⚙️ Settings")
    level = st.selectbox(
        "Your English level",
        ["Beginner", "Intermediate", "Advanced"],
        key="level_select",
    )
    interest = st.text_input(
        "Topics you like",
        value="technology, science",
        key="interest_input",
    )
    num_words = st.slider(
        "Number of new words",
        3,
        10,
        5,
        key="num_words_slider",
    )
    tone = st.selectbox(
        "Teaching style",
        ["Friendly coach", "Exam-focused teacher", "Professional trainer"],
        key="tone_select",
    )
    temperature = st.slider(
        "Creativity",
        0.0,
        1.0,
        0.6,
        0.1,
        key="temp_slider",
    )

# ------------------ PAGE HEADER ------------------
st.title("🗣️ Personalized Vocabulary Builder")
st.markdown("Improve your vocabulary with personalized word suggestions and practice.")
st.divider()

# ------------------ SESSION STATE ------------------
if "saved_words" not in st.session_state:
    st.session_state.saved_words = []
if "current_words" not in st.session_state:
    st.session_state.current_words = ""
if "last_exercise" not in st.session_state:
    st.session_state.last_exercise = ""

# ------------------ HELPERS ------------------
def get_level_instruction(level: str) -> str:
    rules = {
        "Beginner": (
            "Use very simple, high-frequency everyday words (A1–A2). "
            "Avoid rare, technical, abstract, or academic vocabulary."
        ),
        "Intermediate": (
            "Use B1–B2 level words that are a bit more challenging than everyday basics. "
            "Some abstract ideas and phrasal verbs are okay."
        ),
        "Advanced": (
            "Use C1–C2 level vocabulary, including formal, academic, or nuanced words. "
            "You can include idiomatic or specialized terms."
        ),
    }
    return rules.get(level, "")

def generate_words(level, interest, num_words, tone, temperature, previous_words_text):
    if model is None:
        st.error("Gemini model is not available. Ensure `google-generative-ai` is installed and `GEMINI_API_KEY` is set. See DEPLOYMENT.md troubleshooting.")
        return ""

    level_instruction = get_level_instruction(level)
    prompt = f"""
You are an English vocabulary coach.

Learner:
- Level: {level}
- Interests: {interest}
- Teaching style: {tone}

Level rules:
{level_instruction}

Previously suggested words (avoid repeating these words and very close synonyms):
{previous_words_text}

Task:
Suggest exactly {num_words} new English words that follow the level rules and match the learner's interests.

For each word, use this format:

### Word (part of speech)
- Meaning: very clear and learner-friendly
- Example: one natural sentence
- Synonyms: 2–3, if available
- Usage tip: when/where to use it (formality, context, etc.)

Do not add any intro or conclusion. Only output the list of words.
"""
    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": temperature},
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"Error while generating words: {e}")
        return ""

def generate_exercise(saved_sets, temperature):
    if not saved_sets:
        st.warning("Save at least one vocabulary set first.")
        return ""

    if model is None:
        st.error("Gemini model is not available. Ensure `google-generative-ai` is installed and `GEMINI_API_KEY` is set. See DEPLOYMENT.md troubleshooting.")
        return ""

    words_block = "\n\n".join(saved_sets)
    prompt = f"""
You are an English teacher creating a practice worksheet.

Here are vocabulary sets saved by the learner (in Markdown):

{words_block}

Using ONLY these words, create:

1. A matching exercise: words labeled A, B, C... and meanings labeled 1, 2, 3...
2. 5 fill-in-the-blank sentences, with a word bank shown below the sentences.
3. 3 prompts: "Use the word ___ in your own sentence."

Format everything cleanly in Markdown.
Do NOT give the answers.
"""
    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": temperature},
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"Error while generating exercise: {e}")
        return ""

# ------------------ MAIN LAYOUT ------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("✨ Generate New Vocabulary")
    if st.button("🔄 Get New Vocabulary", key="generate_words_btn"):
        previous_text = "\n\n".join(
            st.session_state.saved_words +
            ([st.session_state.current_words] if st.session_state.current_words else [])
        )
        with st.spinner("Generating words..."):
            content = generate_words(
                level,
                interest,
                num_words,
                tone,
                temperature,
                previous_text,
            )
        if content:
            st.session_state.current_words = content
            st.success("Words generated!")

    if st.session_state.current_words:
        st.markdown("### Your New Words")
        st.markdown(st.session_state.current_words)

        if st.button("💾 Save These Words", key="save_words_btn"):
            st.session_state.saved_words.append(st.session_state.current_words)
            st.session_state.current_words = ""
            st.success("Saved!")

    st.subheader("📝 Practice Exercise")
    if st.button("🎯 Generate Practice Exercise", key="generate_exercise_btn"):
        with st.spinner("Creating practice exercise..."):
            exercise = generate_exercise(
                st.session_state.saved_words,
                temperature,
            )
        if exercise:
            st.session_state.last_exercise = exercise

    if st.session_state.last_exercise:
        st.markdown(st.session_state.last_exercise)

with col2:
    st.subheader("📚 Saved Vocabulary Sets")
    if st.session_state.saved_words:
        for i, entry in enumerate(st.session_state.saved_words, 1):
            with st.expander(f"Word Set {i}", expanded=False):
                st.markdown(entry)
    else:
        st.info("No saved words yet.")

st.caption("🧠 Built with Python + Streamlit + Gemini API")
