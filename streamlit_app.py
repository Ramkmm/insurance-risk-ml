import os
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Insurance Risk Predictor", layout="centered")

st.title("🏠 Insurance Risk Prediction System")
st.write("Enter property details to calculate risk score and premium")

# ---------------- INPUTS ----------------
house_age = st.slider("House Age", 0, 50, 10)
location_risk = st.slider("Location Risk (0-1)", 0.0, 1.0, 0.5)
roof_type = st.selectbox("Roof Type", [1, 2, 3])
past_claims = st.slider("Past Claims", 0, 5, 1)
property_value = st.number_input("Property Value", value=500000)

# ---------------- BUTTON ----------------
if st.button("Predict Risk"):

    # ✅ Use ENV or fallback
    url = os.getenv("API_URL", "http://houseinsurancerisk.site/predict")

    data = {
        "house_age": house_age,
        "location_risk": location_risk,
        "roof_type": roof_type,
        "past_claims": past_claims,
        "property_value": property_value
    }

    try:
        # ✅ Add timeout (VERY IMPORTANT)
        response = requests.post(url, json=data, timeout=10)

        # ---------------- SUCCESS ----------------
        if response.status_code == 200:
            result = response.json()

            if "risk_score" in result:
                st.success(f"Risk Score: {result['risk_score']:.4f}")
                st.info(f"Recommended Premium: ₹{result.get('recommended_premium', 0):.2f}")
                st.warning(f"Risk Category: {result.get('risk_category', 'N/A')}")

                # ---------------- FEATURE IMPORTANCE ----------------
                feature_imp = result.get("feature_importance")

                if isinstance(feature_imp, dict) and len(feature_imp) > 0:
                    st.subheader("📊 Feature Impact (Why this risk?)")

                    df = pd.DataFrame({
                        "Feature": list(feature_imp.keys()),
                        "Impact": list(feature_imp.values())
                    }).sort_values(by="Impact", ascending=True)

                    fig, ax = plt.subplots()
                    ax.barh(df["Feature"], df["Impact"])
                    ax.set_xlabel("Impact on Risk Score")
                    ax.set_title("Feature Importance")

                    st.pyplot(fig)

                else:
                    st.info("No feature importance available")

            else:
                st.error(f"Unexpected API Response: {result}")

        # ---------------- API ERROR ----------------
        else:
            try:
                err = response.json()
            except:
                err = response.text

            st.error(f"API Error {response.status_code}: {err}")

    # ---------------- REQUEST FAILURE ----------------
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Try again.")

    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to API. Check server.")

    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")