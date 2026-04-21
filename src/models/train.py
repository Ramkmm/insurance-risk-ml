import os
import logging

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def train_insurance_model(data_path: str, model_path: str) -> bool:
    """
    Train XGBoost classifier for house insurance risk prediction
    and save both model and metadata (feature names, metrics).
    """

    # ---------------- LOAD DATA ----------------
    logger.info(f"📂 Loading data from: {data_path}")

    try:
        df = pd.read_csv(data_path)
        logger.info(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
    except FileNotFoundError:
        logger.error(f"❌ Data file not found: {data_path}")
        return False
    except Exception as e:
        logger.exception(f"❌ Failed to load data: {e}")
        return False

    # ---------------- PREPARE DATA ----------------
    feature_cols = ["house_age", "location_risk", "roof_type", "past_claims", "property_value"]
    target_col = "risk"

    # Check columns
    missing_cols = [c for c in feature_cols + [target_col] if c not in df.columns]
    if missing_cols:
        logger.error(f"❌ Missing required columns in data: {missing_cols}")
        logger.info(f"Available columns: {list(df.columns)}")
        return False

    # Keep only relevant columns and drop NA
    df = df[feature_cols + [target_col]].dropna()

    # Clip to match API validation constraints
    df["roof_type"] = df["roof_type"].clip(1, 5)
    df["property_value"] = df["property_value"].clip(lower=1)
    df["house_age"] = df["house_age"].clip(0, 100)

    X = df[feature_cols]
    # Binary target: high risk = 1 if risk > 0.5
    y = (df[target_col] > 0.5).astype(int)

    logger.info(f"✅ Clean data shape: {X.shape}")
    logger.info("📊 Target distribution:\n" + y.value_counts(normalize=True).round(3).to_string())

    # ---------------- TRAIN / TEST SPLIT ----------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ---------------- TRAIN MODEL ----------------
    logger.info("🚀 Training XGBoost classifier...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss",
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    # ---------------- EVALUATE ----------------
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)

    logger.info(f"✅ Train accuracy: {train_acc:.3f}")
    logger.info(f"✅ Test accuracy:  {test_acc:.3f}")
    logger.info("📄 Classification report (test):\n" +
                classification_report(y_test, y_test_pred, digits=3))

    # ---------------- SAVE MODEL & METADATA ----------------
    try:
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        # Save model
        joblib.dump(model, model_path)
        logger.info(f"💾 Model saved to: {model_path}")

        # Save metadata for feature importance in API
        metadata = {
            "feature_names": feature_cols,
            "target_name": target_col,
            "train_accuracy": float(train_acc),
            "test_accuracy": float(test_acc),
            "n_samples": int(len(df)),
            "model_type": "XGBClassifier",
        }

        metadata_path = model_path.replace(".pkl", "_metadata.pkl")
        joblib.dump(metadata, metadata_path)
        logger.info(f"💾 Metadata saved to: {metadata_path}")

        return True

    except Exception as e:
        logger.exception(f"❌ Failed to save model/metadata: {e}")
        return False


if __name__ == "__main__":
    # Project root (absolute, Windows safe)
    PROJECT_ROOT = r"C:\Users\DELL\Desktop\sample_project\DSMLHINPROJECT\insurance-risk-ml"

    DATA_PATH = os.path.join(PROJECT_ROOT, "data", "insurance_data.csv")
    MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "risk_model1.pkl")

    print("🏠 Training Insurance Risk Model")
    print(f"📊 Data:  {DATA_PATH}")
    print(f"💾 Model: {MODEL_PATH}")
    print("-" * 60)

    success = train_insurance_model(DATA_PATH, MODEL_PATH)

    if success:
        print("\n🎉 MODEL TRAINED & SAVED!")
        print("Run FastAPI: uvicorn app:app --reload  (from src\\api)")
    else:
        print("\n❌ Training failed. Check logs and that data file exists at:")
        print(DATA_PATH)