import streamlit as st
import requests

st.set_page_config(page_title="Insurance Risk Predictor")

st.title("🏠 Insurance Risk Prediction System")

st.write("Enter property details to calculate risk score and premium")

# Input fields
house_age = st.slider("House Age", 0, 50, 10)
location_risk = st.slider("Location Risk (0-1)", 0.0, 1.0, 0.5)
roof_type = st.selectbox("Roof Type", [1, 2, 3])
past_claims = st.slider("Past Claims", 0, 5, 1)
property_value = st.number_input("Property Value", value=500000)

# Button
if st.button("Predict Risk"):
    
    url = "https://insurance-risk-ml.onrender.com/predict"

    data = {
        "house_age": house_age,
        "location_risk": location_risk,
        "roof_type": roof_type,
        "past_claims": past_claims,
        "property_value": property_value
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()

        st.success(f"Risk Score: {result['risk_score']:.2f}")
        st.info(f"Recommended Premium: ₹{result['recommended_premium']}")
    else:
        st.error("API Error")