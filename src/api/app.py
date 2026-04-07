from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("models/risk_model.pkl")

@app.get("/")
def home():
    return {"message": "Insurance Risk API Running"}

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])

    risk_score = model.predict_proba(df)[0][1]

    premium = 500 + (risk_score * 2000)

    return {
        "risk_score": float(risk_score),
        "recommended_premium": float(premium)
    }