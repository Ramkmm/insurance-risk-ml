import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Insurance Risk Predictor", layout="centered")

st.title("🏠 Insurance Risk Prediction System")
st.write("Enter property details to calculate risk score and recommended premium.")

# ---------------- INPUTS ----------------
house_age = st.slider("House Age (years)", 0, 100, 10)
location_risk = st.slider("Location Risk (0–1)", 0.0, 1.0, 0.5, step=0.01)
roof_type = st.selectbox("Roof Type (1–5)", options=[1, 2, 3, 4, 5])
past_claims = st.slider("Past Claims", 0, 10, 1)
property_value = st.number_input("Property Value (₹)", min_value=1.0, value=500000.0, step=10000.0)

# ---------------- PREDICT BUTTON ----------------
if st.button("Predict Risk"):

    # Local default; override with API_URL env in prod
    api_url = os.getenv("API_URL", "http://localhost:8000/predict")

    payload = {
        "house_age": int(house_age),
        "location_risk": float(location_risk),
        "roof_type": int(roof_type),
        "past_claims": int(past_claims),
        "property_value": float(property_value),
    }

    st.write("📨 Sending payload to API:")
    st.json(payload)

    try:
        response = requests.post(api_url, json=payload, timeout=10)

        # ---------------- SUCCESS ----------------
        if response.status_code == 200:
            result = response.json()

            if "risk_score" not in result:
                st.error("Unexpected API response format (missing 'risk_score').")
                st.json(result)
            else:
                risk_score = float(result["risk_score"])
                st.success(f"Risk Score: {risk_score:.4f}")

                # Numeric premium from API, format as rupees
                premium_val = float(result.get("recommended_premium", 0.0))
                st.info(f"Recommended Premium: ₹{premium_val:,.2f}")

                st.warning(f"Risk Category: {result.get('risk_category', 'N/A')}")

                # ---------------- FEATURE IMPORTANCE GRAPH ----------------
                feature_imp = result.get("feature_importance")

                if isinstance(feature_imp, dict) and feature_imp:
                    st.subheader("📊 Feature Impact (Why this risk?)")

                    df = (
                        pd.DataFrame(
                            {"Feature": list(feature_imp.keys()),
                             "Impact": list(feature_imp.values())}
                        )
                        .sort_values(by="Impact", ascending=True)
                    )

                    fig, ax = plt.subplots()
                    ax.barh(df["Feature"], df["Impact"])
                    ax.set_xlabel("Relative Importance")
                    ax.set_title("Model Feature Importance")
                    plt.tight_layout()  # nicer layout in Streamlit
                    st.pyplot(fig)
                else:
                    st.info("No feature importance available from API.")

        # ---------------- API ERROR ----------------
        else:
            try:
                err = response.json()
            except Exception:
                err = response.text

            st.error(f"API Error {response.status_code}")
            st.code(err, language="json")

    # ---------------- NETWORK / OTHER ERRORS ----------------
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Try again.")

    except requests.exceptions.ConnectionError:
        st.error(f"🔌 Cannot connect to API at: {api_url}. Is the server running?")

    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")