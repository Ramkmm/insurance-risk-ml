from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("models/risk_model.pkl")

@app.get("/")
def home():
    return {"message": "Insurance Risk API Running"}

from fastapi import FastAPI
import joblib
import pandas as pd
import os
import datetime
import json

app = FastAPI()

# Load model
model_path = os.path.join(os.path.dirname(__file__), "../../models/risk_model.pkl")
model = joblib.load(model_path)

@app.get("/")
def home():
    return {"message": "Insurance Risk API Running"}

@app.post("/predict")
def predict(data: dict):

    # ✅ MUST be indented
    model_features = ["house_age", "location_risk", "roof_type", "past_claims", "property_value"]

    filtered_data = {key: data[key] for key in model_features}

    df = pd.DataFrame([filtered_data])

    # Prediction
    risk_score = model.predict_proba(df)[0][1]
    premium = 500 + (risk_score * 2000)

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
        "risk_category": category
    }