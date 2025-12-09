import joblib
import numpy as np

MODEL_PATH = "app_backend/models/model.pkl"
SCALER_PATH = "app_backend/models/scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# Example patient data
new_patient = np.array([[2, 120, 70, 30, 100, 25.0, 0.5, 30]])

new_patient_scaled = scaler.transform(new_patient)
prediction = model.predict(new_patient_scaled)
probability = model.predict_proba(new_patient_scaled)[:, 1]

print(f"Predicted outcome: {prediction[0]} (1 = diabetes, 0 = no diabetes)")
print(f"Probability of having diabetes: {probability[0]:.2f}")
