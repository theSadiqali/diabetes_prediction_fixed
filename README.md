# Diabetes Prediction Fixed Project (with Chatbot)

This is a fixed, minimal working skeleton of your project with a simple retrieval-based chatbot.

Run the backend:

```bash
python -m venv .venv
source .venv/bin/activate   # or .\.venv\Scripts\activate on Windows
pip install -r requirements.txt

# initialize DB (optional)
python -c "from app_backend.db import init_db; init_db()"

# run server
uvicorn app_backend.main:app --reload
```

The /chat endpoint expects JSON {"question": "..."} and returns a retrieval-based answer from verified sources (WHO, ADA, CDC, NHS, Mayo Clinic). Grammar correction uses language-tool-python if installed.
