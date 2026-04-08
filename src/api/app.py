from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI()

# ✅ LOAD MODEL
model_path = os.path.join(os.path.dirname(__file__), "../../models/risk_model.pkl")
model = joblib.load(model_path)

# ✅ DEFINE INPUT CLASS FIRST
class InsuranceInput(BaseModel):
    house_age: int
    location_risk: float
    roof_type: int
    past_claims: int
    property_value: float

# ✅ HOME ROUTE
@app.get("/")
def home():
    return {"message": "Insurance Risk API Running"}

# ✅ PREDICT ROUTE
@app.post("/predict")
def predict(data: InsuranceInput):

    data = data.dict()

    model_features = ["house_age", "location_risk", "roof_type", "past_claims", "property_value"]
    filtered_data = {key: data[key] for key in model_features}

    df = pd.DataFrame([filtered_data])

    risk_score = model.predict_proba(df)[0][1]
    premium = 500 + (risk_score * 2000)

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