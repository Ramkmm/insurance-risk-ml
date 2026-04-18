import os
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ---------------- INPUT ----------------
class InsuranceInput(BaseModel):
    house_age: int
    location_risk: float
    roof_type: int
    past_claims: int
    property_value: float

# ---------------- LOAD MODEL ----------------
MODEL_PATH = os.path.join(os.getcwd(), "models", "risk_model1.pkl")

print("Loading model from:", MODEL_PATH)
print("🔥 VERSION V3 - APP.PY UPDATED 🔥")
try:
    print("Files in models:", os.listdir("models"))
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Model loading failed: {e}")
    model = None

# ---------------- API ----------------
@app.get("/")
def home():
    return {"message": "Insurance Risk API running 🚀"}

@app.post("/predict")
def predict(data: InsuranceInput):
    if model is None:
        return {"error": "Model not loaded"}

    input_data = [[
        data.house_age,
        data.location_risk,
        data.roof_type,
        data.past_claims,
        data.property_value
    ]]

    prediction = model.predict(input_data)[0]

    return {
        "risk_score": float(prediction),
        "risk_category": "Low Risk" if prediction < 0.5 else "High Risk"
    }