import shap
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os
import numpy as np

app = FastAPI()

# =========================
# LOAD MODEL (Dynamic Path)
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "models", "risk_model1.pkl")

model = joblib.load(MODEL_PATH)

# SHAP Explainer (GLOBAL - correct)
explainer = shap.TreeExplainer(model)

# =========================
# INPUT SCHEMA
# =========================
class InsuranceInput(BaseModel):
    house_age: int
    location_risk: float
    roof_type: int
    past_claims: int
    property_value: float

# =========================
# HOME ROUTE
# =========================
@app.get("/")
def home():
    return {"message": "Insurance Risk API Running"}

# =========================
# PREDICT ROUTE
# =========================
@app.post("/predict")
def predict(data: InsuranceInput):

    # Convert input to dict
    data = data.dict()

    # Ensure correct feature order
    model_features = [
        "house_age",
        "location_risk",
        "roof_type",
        "past_claims",
        "property_value"
    ]

    # Create DataFrame
    df = pd.DataFrame([[data[f] for f in model_features]], columns=model_features)

    # =========================
    # Prediction
    # =========================
    risk_score = model.predict_proba(df)[0][1]
    premium = 500 + (risk_score * 2000)

    # =========================
    # SHAP Explainability
    # =========================
    shap_values = explainer.shap_values(df)

    # Convert SHAP values to readable importance
    shap_vals = np.abs(shap_values[0])  # absolute contribution
    shap_vals = shap_vals / shap_vals.sum()  # normalize

    feature_impact = dict(zip(model_features, shap_vals.tolist()))

    # =========================
    # Risk Category
    # =========================
    if risk_score < 0.3:
        category = "Low Risk"
    elif risk_score < 0.7:
        category = "Medium Risk"
    else:
        category = "High Risk"

    # =========================
    # Response
    # =========================
    return {
        "risk_score": float(risk_score),
        "recommended_premium": float(premium),
        "risk_category": category,
        "feature_importance": feature_impact
    }