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

---

## Troubleshooting

If your Streamlit deployment fails with an error like:

```
ModuleNotFoundError: No module named 'google.generativeai'
```

Try the following:

1. Ensure `google-generative-ai` is listed in `requirements.txt`. If not, add it and push the change.

2. Make sure your Python runtime is compatible with the SDK. Some cloud hosts use a newer Python version by default; pin the runtime to a compatible version (e.g., `python-3.10`) in `runtime.txt`, then redeploy.

3. Manually test locally:
   - python -m venv venv
   - venv\Scripts\activate  (Windows)
   - pip install -r requirements.txt
   - pip install google-generative-ai
   - streamlit run app.py

4. If installation fails on the platform, check the deploy logs for details and consider using a supported Python version (see step 2).

If you're still stuck, share the log output and I can help debug further.
