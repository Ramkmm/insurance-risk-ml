import pandas as pd
from xgboost import XGBClassifier
import joblib

# Load data
df = pd.read_csv(r"C:\Users\DELL\Desktop\sample_project\DSMLHINPROJECT\insurance-risk-ml\data\sample_data.csv")

X = df.drop("claim_occurred", axis=1)
y = df["claim_occurred"]

# Train model
model = XGBClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "models/risk_model.pkl")

print("✅ Model trained and saved!")