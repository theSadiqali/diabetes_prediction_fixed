from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app_backend.api.predict import router as predict_router
from app_backend.api.chat import router as chat_router

app = FastAPI(title="Diabetes Prediction + Chatbot API")

# Include routers
app.include_router(predict_router, prefix="/predict", tags=["Predict"])
app.include_router(chat_router, prefix="/chat", tags=["Chatbot"])

# Static files
app.mount("/static", StaticFiles(directory="app_backend/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app_backend/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/status")
def status():
    return {"status": "ok", "service": "Diabetes Prediction API"}
