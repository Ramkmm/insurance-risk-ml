import os
import joblib
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------- FASTAPI CONFIG ----------------
app = FastAPI(
    title="Insurance Risk API",
    version="1.0.0",
    openapi_version="3.0.2"
)

# ---------------- INPUT MODEL ----------------
class InsuranceInput(BaseModel):
    house_age: int = Field(..., ge=0, le=100)
    location_risk: float = Field(..., ge=0, le=1)
    roof_type: int = Field(..., ge=1, le=5)
    past_claims: int = Field(..., ge=0, le=10)
    property_value: float = Field(..., gt=0)

# ---------------- LOAD MODEL ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ safer absolute path (Docker compatible)
MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../models/risk_model1.pkl"))

logger.info(f"📦 Model path: {MODEL_PATH}")

model = None

def load_model():
    global model
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

        model = joblib.load(MODEL_PATH)
        logger.info("✅ Model loaded successfully")

    except Exception as e:
        logger.exception(f"❌ Model loading failed: {e}")
        model = None

# ✅ Load model at startup
@app.on_event("startup")
def startup_event():
    logger.info("🚀 Starting Insurance API...")
    load_model()

# ---------------- HEALTH CHECK ----------------
@app.get("/health")
def health():
    return {
        "status": "ok" if model else "error",
        "model_loaded": model is not None
    }

# ---------------- ROOT ----------------
@app.get("/")
def home():
    return {"message": "Insurance Risk API running 🚀"}

# ---------------- PREDICT ----------------
@app.post("/predict")
def predict(data: InsuranceInput):
    logger.info(f"📥 Incoming request: {data}")

    if model is None:
        logger.error("Model not loaded")
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        input_data = [[
            data.house_age,
            data.location_risk,
            data.roof_type,
            data.past_claims,
            data.property_value
        ]]

        prediction = model.predict(input_data)[0]
        risk_score = float(prediction)

        # ✅ premium logic
        recommended_premium = data.property_value * (0.01 + risk_score * 0.05)

        response = {
            "risk_score": round(risk_score, 4),
            "risk_category": "Low Risk" if risk_score < 0.5 else "High Risk",
            "recommended_premium": round(recommended_premium, 2)
        }

        logger.info(f"📤 Response: {response}")
        return response

    except Exception as e:
        logger.exception(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction error")