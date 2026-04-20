import os
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Insurance Risk Predictor")

st.title("🏠 Insurance Risk Prediction System")
st.write("Enter property details to calculate risk score and premium")

# Inputs
house_age = st.slider("House Age", 0, 50, 10)
location_risk = st.slider("Location Risk (0-1)", 0.0, 1.0, 0.5)
roof_type = st.selectbox("Roof Type", [1, 2, 3])
past_claims = st.slider("Past Claims", 0, 5, 1)
property_value = st.number_input("Property Value", value=500000)

# Button
if st.button("Predict Risk"):

    url = os.getenv("API_URL", "http://houseinsurancerisk.site/predict")

    data = {
        "house_age": house_age,
        "location_risk": location_risk,
        "roof_type": roof_type,
        "past_claims": past_claims,
        "property_value": property_value
    }

    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            result = response.json()

            # ✅ Handle correct response
            if "risk_score" in result:
                st.success(f"Risk Score: {result['risk_score']:.4f}")
                st.info(f"Recommended Premium: ₹{result['recommended_premium']:.2f}")
                st.warning(f"Risk Category: {result['risk_category']}")

                # ✅ Feature Importance
                feature_imp = result.get("feature_importance", {})

                if feature_imp:
                    st.subheader("📊 Feature Impact (Why this risk?)")

                    features = list(feature_imp.keys())
                    values = list(feature_imp.values())

                    fig, ax = plt.subplots()
                    ax.barh(features, values)
                    ax.set_xlabel("Impact on Risk Score")
                    ax.set_ylabel("Features")
                    ax.set_title("Feature Importance")

                    st.pyplot(fig)
                else:
                    st.warning("No feature importance data available")

            else:
                st.error(f"API Response Error: {result}")

        else:
            st.error(f"API Error: {response.status_code}")

    except Exception as e:
        st.error(f"Request Failed: {e}")