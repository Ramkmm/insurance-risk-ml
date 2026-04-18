import os
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

# ✅ Proper FastAPI config (fix Swagger issue)
app = FastAPI(
    title="Insurance Risk API",
    version="1.0.0",
    openapi_version="3.0.2"
)

# ---------------- INPUT ----------------
class InsuranceInput(BaseModel):
    house_age: int
    location_risk: float
    roof_type: int
    past_claims: int
    property_value: float

# ---------------- LOAD MODEL ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../../models/risk_model1.pkl")

print("🔥 VERSION V4 - FIXED PATH 🔥")
print("Working dir:", os.getcwd())
print("Model path:", MODEL_PATH)

try:
    print("Files in /app:", os.listdir("/app"))
    print("Files in models:", os.listdir("/app/models"))
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