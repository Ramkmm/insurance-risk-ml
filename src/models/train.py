import pandas as pd
import numpy as np
from xgboost import XGBClassifier
import joblib
import os
import logging
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def train_insurance_model(data_path, model_path):
    """
    Train XGBoost classifier for house insurance risk prediction
    """
    
    # ---------------- LOAD DATA ----------------
    logger.info(f"Loading data from: {data_path}")
    
    try:
        df = pd.read_csv(data_path)
        logger.info(f"Loaded {len(df)} rows")
    except FileNotFoundError:
        logger.error(f"Data file not found: {data_path}")
        return False
    
    # ---------------- PREPARE DATA ----------------
    feature_cols = ["house_age", "location_risk", "roof_type", "past_claims", "property_value"]
    target_col = "risk"
    
    # Check columns
    if not all(col in df.columns for col in feature_cols + [target_col]):
        logger.error("Missing required columns")
        return False
    
    df = df[feature_cols + [target_col]].dropna()
    df['roof_type'] = df['roof_type'].clip(1, 5)
    df['property_value'] = df['property_value'].clip(lower=1)
    df['house_age'] = df['house_age'].clip(0, 100)
    
    X = df[feature_cols]
    y = (df[target_col] > 0.5).astype(int)
    
    logger.info(f"Clean data: {X.shape}")
    
    # ---------------- TRAIN MODEL ----------------
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = XGBClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # ---------------- RESULTS ----------------
    test_acc = model.score(X_test, y_test)
    logger.info(f"Test Accuracy: {test_acc:.3f}")
    
    # ---------------- SAVE ----------------
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    logger.info(f"SAVED: {model_path}")
    
    return True

if __name__ == "__main__":
    # ✅ FIXED: Use raw strings + os.path
    PROJECT_ROOT = r"C:\Users\DELL\Desktop\sample_project\DSMLHINPROJECT\insurance-risk-ml"
    
    DATA_PATH = os.path.join(PROJECT_ROOT, "data", "insurance_data.csv")
    MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "risk_model1.pkl")
    
    print("🏠 Training Insurance Risk Model")
    print(f"📊 Data: {DATA_PATH}")
    print(f"💾 Model: {MODEL_PATH}")
    
    success = train_insurance_model(DATA_PATH, MODEL_PATH)
    
    if success:
        print("\n🎉 MODEL TRAINED & SAVED!")
        print("Run FastAPI: uvicorn app:app --reload")
    else:
        print("\n❌ Check data file exists at:", DATA_PATH)