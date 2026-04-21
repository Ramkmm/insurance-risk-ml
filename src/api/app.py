import os
import joblib
import logging
import numpy as np
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
    title="House Insurance Risk API 🚀",
    version="1.2.0",
    description="Predict house insurance risk using ML model",
)

# ---------------- INPUT MODEL ----------------
class InsuranceInput(BaseModel):
    house_age: int = Field(..., ge=0, le=100, description="House age in years")
    location_risk: float = Field(..., ge=0, le=1, description="Location risk score (0-1)")
    roof_type: int = Field(..., ge=1, le=5, description="Roof type (1–5)")
    past_claims: int = Field(..., ge=0, le=10, description="Number of past claims")
    property_value: float = Field(..., gt=0, description="Property value in rupees")

# ---------------- MODEL CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "models", "risk_model1.pkl")
METADATA_PATH = MODEL_PATH.replace(".pkl", "_metadata.pkl")

model = None
metadata = None  # to hold feature names etc.

def load_model():
    global model, metadata
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

        model = joblib.load(MODEL_PATH)
        logger.info("✅ Model loaded successfully")

        if os.path.exists(METADATA_PATH):
            metadata = joblib.load(METADATA_PATH)
            logger.info(f"✅ Metadata loaded from {METADATA_PATH}")
        else:
            metadata = None
            logger.warning(f"⚠️ Metadata file not found at {METADATA_PATH}. Feature importance may be unavailable.")

    except Exception as e:
        logger.exception(f"❌ Model loading failed: {e}")
        model = None
        metadata = None

@app.on_event("startup")
def startup_event():
    logger.info("🚀 Starting House Insurance Risk API...")
    load_model()

# ---------------- HEALTH ----------------
@app.get("/health")
def health():
    return {
        "status": "healthy" if model is not None else "degraded",
        "model_loaded": model is not None,
        "model_path": MODEL_PATH,
        "model_exists": os.path.exists(MODEL_PATH),
        "metadata_loaded": metadata is not None,
        "metadata_path": METADATA_PATH,
        "metadata_exists": os.path.exists(METADATA_PATH),
    }

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {
        "message": "House Insurance Risk API running 🚀",
        "docs": "/docs",
        "health": "/health",
        "predict": "POST /predict",
        "version": "1.2.0",
    }

# ---------------- PREDICT ----------------
@app.post("/predict")
def predict(data: InsuranceInput):
    logger.info(f"📥 Prediction request: {data.dict()}")

    if model is None:
        raise HTTPException(status_code=503, detail="Model not available. Check /health")

    try:
        # Build feature vector in same order as training
        input_data = np.array([[
            data.house_age,
            data.location_risk,
            data.roof_type,
            data.past_claims,
            data.property_value
        ]], dtype=np.float64)

        prediction = model.predict(input_data)[0]
        risk_score = float(prediction)

        # Clamp risk score between 0 and 1
        risk_score = max(0.0, min(1.0, risk_score))

        # Premium calculation (INR)
        base_rate = 0.01
        risk_multiplier = 0.05 + risk_score * 0.10
        value = data.property_value * (base_rate + risk_multiplier)
        recommended_premium = round(value, 2)  # numeric, in rupees

        # ---------------- FEATURE IMPORTANCE ----------------
        feature_importance = None
        try:
            if hasattr(model, "feature_importances_"):
                importances = model.feature_importances_

                # Get feature names from metadata or fallback
                if metadata and "feature_names" in metadata:
                    feature_names = metadata["feature_names"]
                else:
                    # Fallback: hard-code in same order as training
                    feature_names = [
                        "house_age",
                        "location_risk",
                        "roof_type",
                        "past_claims",
                        "property_value",
                    ]

                # Ensure lengths match
                if len(importances) == len(feature_names):
                    feature_importance = {
                        name: float(imp)
                        for name, imp in zip(feature_names, importances)
                    }
                else:
                    logger.warning(
                        f"Feature importance length mismatch: "
                        f"{len(importances)} importances vs {len(feature_names)} names"
                    )
                    feature_importance = None
        except Exception as fe:
            logger.warning(f"Failed to compute feature importance: {fe}")
            feature_importance = None

        response = {
            "risk_score": round(risk_score, 4),
            "risk_category": (
                "Low Risk" if risk_score < 0.3
                else "Medium Risk" if risk_score < 0.7
                else "High Risk"
            ),
            "recommended_premium": recommended_premium,
            "property_value": round(float(data.property_value), 2),
            "input_summary": data.dict(),
            "feature_importance": feature_importance,  # ✅ for Streamlit graph
        }

        logger.info(f"📤 Response: {response}")
        return response

    except Exception as e:
        logger.exception(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction error")