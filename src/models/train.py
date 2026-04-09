import pandas as pd
from xgboost import XGBClassifier
import joblib

# Load data
df = pd.read_csv(r"C:\Users\DELL\Desktop\sample_project\DSMLHINPROJECT\insurance-risk-ml\data\insurance_data.csv")

# Features & target
X = df[["house_age", "location_risk", "roof_type", "past_claims", "property_value"]]
y = (df["risk"] > 0.5).astype(int)

# Train model
model = XGBClassifier()
model.fit(X, y)

# Save model
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "models", "risk_model2.pkl")

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

joblib.dump(model, MODEL_PATH)

print("Model retrained!")