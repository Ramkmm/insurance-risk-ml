from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI()

# -------------------------------
# 📌 Input Schema
# -------------------------------
class InsuranceInput(BaseModel):
    house_age: int
    location_risk: float
    roof_type: int
    past_claims: int
    property_value: float


# -------------------------------
# 📌 Load Model (Docker-safe path)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../models/risk_model.pkl")
print("Loading model from:", MODEL_PATH)

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Model loading failed: {e}")
    model = None


# -------------------------------
# 📌 Health Check
# -------------------------------
@app.get("/")
def home():
    return {"message": "Insurance Risk API is running 🚀"}


# -------------------------------
# 📌 Prediction API
# -------------------------------
@app.post("/predict")
def predict(data: dict):
    global model

    if model is None:
        return {"error": "Model not loaded"}

    try:
        features = np.array([[
            data["house_age"],
            data["location_risk"],
            data["roof_type"],
            data["past_claims"],
            data["property_value"]
        ]])

        prediction = model.predict(features)[0]

        # ✅ Dummy feature importance (replace later with SHAP)
        feature_importance = {
            "house_age": 0.15,
            "location_risk": 0.52,
            "roof_type": 0.01,
            "past_claims": 0.29,
            "property_value": 0.03
        }

        return {
            "risk_score": float(prediction),
            "recommended_premium": float(500 + prediction * 1000),
            "risk_category": "Low Risk" if prediction < 0.5 else "High Risk",
            "feature_importance": feature_importance   # ✅ ADD THIS
        }

    except Exception as e:
        return {"error": str(e)}