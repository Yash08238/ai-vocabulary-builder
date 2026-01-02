Streamlit Deployment Guide

Local testing

1. Create and activate a virtual environment:
   - python -m venv venv
   - Windows: venv\Scripts\activate
2. Install dependencies:
   - pip install -r requirements.txt
3. Create a `.env` file in the project root (DO NOT commit this file). Example `.env`:
   GEMINI_API_KEY=your_api_key_here

   Alternatively, set the environment variable directly:
   - Windows (PowerShell): $env:GEMINI_API_KEY = "your_api_key"
   - Linux/macOS: export GEMINI_API_KEY="your_api_key"
4. Run the app:
   - streamlit run app.py

Note: The app will load `.env` automatically during local development using `python-dotenv`. Ensure `.env` is added to `.gitignore` to avoid committing secret keys.
Deploy to Streamlit Cloud (https://streamlit.io)

1. Push this repository to GitHub if it's not already.
2. On Streamlit Cloud, create a new app and point it to the repository and branch.
3. In the app's Settings → Secrets, add:
   - GEMINI_API_KEY = your_real_api_key
4. Set the Python runtime in project settings if necessary (project uses runtime.txt).
5. Deploy and monitor the logs on the Streamlit Cloud dashboard.

Notes

- Do NOT commit real API keys to the repository. Use Streamlit's Secrets UI for production or CI secure storage.
- If you prefer local .env files, consider using python-dotenv and loading it in `app.py` for local convenience.
