from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

router = APIRouter()

# ----------------------------
# Load model & scaler
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

try:
    model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
    scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
except Exception as e:
    print("Warning: could not load model or scaler:", e)
    model, scaler = None, None

# ----------------------------
# Input schema
# ----------------------------
class DiabetesInput(BaseModel):
    Pregnancies: float
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: float

# ----------------------------
# Predict endpoint
# ----------------------------
@router.post("/")
def predict(data: DiabetesInput):
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model or scaler not loaded.")
    
    try:
        # Ensure correct feature order
        X = np.array([[data.Pregnancies, data.Glucose, data.BloodPressure, data.SkinThickness,
                       data.Insulin, data.BMI, data.DiabetesPedigreeFunction, data.Age]])
        X_scaled = scaler.transform(X)
        
        # Predict probability
        prob = model.predict_proba(X_scaled)[0][1]  # probability of diabetes
        return {"probability": float(prob)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
