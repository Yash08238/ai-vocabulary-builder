# 🗣️ Personalized Vocabulary Builder

A simple and interactive English vocabulary learning app built using **Python**, **Streamlit**, and **Google Gemini API**.  
The app generates personalized vocabulary lists based on user level and interests, and provides practice exercises to reinforce learning.

---

## ✨ Features

- Generate vocabulary based on:
  - English proficiency level (Beginner / Intermediate / Advanced)
  - Topic interests
  - Number of words
- Avoids repeating previously generated vocabulary
- Save vocabulary sets locally during session
- Generate practice exercises, including:
  - Matching activities
  - Fill-in-the-blank questions
  - Sentence creation prompts
- Clean and user-friendly interface

---

## 🧠 How It Works

1. Select your level and interests from the sidebar  
2. Generate new vocabulary  
3. Save the generated words to your learning list  
4. Create personalized exercises based on saved vocabulary  

Created by **Yash Chauhan**.

---

## 🚀 Deploy to Streamlit

To run locally:

1. Install dependencies: `pip install -r requirements.txt`
2. Set your Gemini API key in an environment variable called `GEMINI_API_KEY` or use `secrets.example.toml` as a reference
3. Run: `streamlit run app.py`

To deploy on Streamlit Cloud:

1. Push this repository to GitHub
2. Create a new app on Streamlit Cloud and point it to this repo
3. In the app's Settings → Secrets, add `GEMINI_API_KEY` (do NOT commit your real key)
4. Streamlit will detect `app.py` and `requirements.txt` and deploy the app

See `DEPLOYMENT.md` for more details and troubleshooting.
