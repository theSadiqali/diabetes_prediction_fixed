from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from pathlib import Path
import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# -----------------------------------------------------
# Load .env
# -----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # app_backend
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in .env")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)

router = APIRouter()

# -----------------------------------------------------
# Input / Output Models
# -----------------------------------------------------
class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, str]]

# -----------------------------------------------------
# Load Knowledge Base
# -----------------------------------------------------
KN_DIR = BASE_DIR / "knowledge"
DOCS, DOC_NAMES = [], []

if KN_DIR.exists():
    for f in sorted(KN_DIR.glob("*.txt")):
        DOC_NAMES.append(f.stem)
        with open(f, "r", encoding="utf-8") as fh:
            DOCS.append(fh.read())

if not DOCS:
    DOCS = ["No knowledge base available."]
    DOC_NAMES = ["knowledge"]

VECT = TfidfVectorizer(stop_words="english").fit(DOCS)
DOC_VECS = VECT.transform(DOCS)

def retrieve(query: str, k: int = 3):
    qv = VECT.transform([query])
    sims = cosine_similarity(qv, DOC_VECS)[0]
    idx = sims.argsort()[::-1][:k]

    return [
        {
            "name": DOC_NAMES[i],
            "score": float(sims[i]),
            "text": DOCS[i],
        }
        for i in idx
    ]

# -----------------------------------------------------
# Extract Gemini Text Safely
# -----------------------------------------------------
def extract_text(resp):
    try:
        cand = resp["candidates"][0]
        parts = cand["content"]["parts"]
        return parts[0]["text"]
    except Exception:
        return "I'm sorry, I couldn't process the response."

# -----------------------------------------------------
# Gemini Integration — FIXED & UPGRADED
# -----------------------------------------------------
def ask_gemini(prompt: str):
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 2048,     # ← BIG FIX
            "temperature": 0.7,
            "topP": 0.9,
            "topK": 40,
        },

        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_CIVIC_INTEGRITY", "threshold": "BLOCK_NONE"}
        ]

       


        
    }

    params = {"key": GEMINI_API_KEY}

    try:
        r = requests.post(GEMINI_URL, json=payload, params=params, timeout=15)
        data = r.json()

        print("GEMINI RAW RESPONSE:", data)

        if r.status_code != 200:
            raise Exception(data)

        return extract_text(data)

    except Exception as e:
        print("Gemini API error:", e)
        return None

# -----------------------------------------------------
# Chat Endpoint
# -----------------------------------------------------
@router.post("/", response_model=ChatResponse)
def chat(req: ChatRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is empty")

    hits = retrieve(question, k=3)
    context_text = "\n\n".join([h["text"] for h in hits])

    options_text = (
        "Provide guidance using these options if relevant:\n"
        "1. Lifestyle changes (diet, exercise)\n"
        "2. Medication guidance\n"
        "3. Monitoring blood glucose\n"
        "4. Preventing complications\n"
        "5. Resources (ADA, CDC, NHS, WHO)\n"
        "6. Other advice\n"
    )

  


    prompt = (
        "You are a professional AI medical assistant specializing in diabetes. ANswer every question like you are a human. and answer it like you are diabetes doctor. and your name is ali. your AI Chatbot\n"
        "Use the following reference knowledge:\n"
        f"{context_text}\n\n"
        f"{options_text}\n"
        f"User question: {question}\n"
        "Give a short, medically helpful answer in 3–4 sentences maximum. "
        "Do NOT write long explanations."
        "Write in the end in short. This chatbot is only Educational purpose."
    )


    # Ask Gemini
    answer = ask_gemini(prompt) or "I'm sorry, I could not get a response."

    sources = [
        {"source": h["name"], "score": f"{h['score']:.4f}"}
        for h in hits
    ]

    return {"answer": answer, "sources": sources}
