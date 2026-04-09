from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI()

# Load model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "models", "risk_model1.pkl")

model = joblib.load(MODEL_PATH)

# Input schema
class InsuranceInput(BaseModel):
    house_age: int
    location_risk: float
    roof_type: int
    past_claims: int
    property_value: float

@app.get("/")
def home():
    return {"message": "Insurance Risk API Running"}

@app.post("/predict")
def predict(data: InsuranceInput):

    data = data.dict()

    model_features = [
        "house_age", "location_risk",
        "roof_type", "past_claims", "property_value"
    ]

    df = pd.DataFrame([[data[f] for f in model_features]], columns=model_features)

    # Prediction
    risk_score = model.predict_proba(df)[0][1]
    premium = 500 + (risk_score * 2000)

    # ✅ SIMPLE FEATURE IMPORTANCE (REPLACEMENT FOR SHAP)
    feature_impact = dict(zip(
        model_features,
        model.feature_importances_.tolist()
    ))

    # Risk category
    if risk_score < 0.3:
        category = "Low Risk"
    elif risk_score < 0.7:
        category = "Medium Risk"
    else:
        category = "High Risk"

    return {
        "risk_score": float(risk_score),
        "recommended_premium": float(premium),
        "risk_category": category,
        "feature_importance": feature_impact
    }