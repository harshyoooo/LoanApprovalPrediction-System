import streamlit as st
import requests
from typing import Union, Dict, Any
import requests
url = "http://127.0.0.1:8000/api/predict/"

st.title("📊 Loan Approval Predictor")

model = st.selectbox("Choose model", ["dt", "xgboost", "nn","random forest"])

inputs = {
    "person_age": st.number_input("Age", 18, 100),
    "person_income": st.number_input("Income", 0),
    "person_home_ownership": st.selectbox("Home Ownership", ["RENT", "OWN", "MORTGAGE", "OTHER"]),
    "person_emp_length": st.number_input("Employment Length (years)", 0, 50),
    "loan_grade": st.selectbox("Loan Grade", ["A", "B", "C", "D", "E", "F", "G"]),
    "loan_amnt": st.number_input("Loan Amount", 500, 50000),
    "loan_int_rate": st.number_input("Interest Rate (%)", 1.0, 50.0),
    "loan_percent_income": st.number_input("Loan % of Income", 0.0, 1.0),
    "cb_person_default_on_file": st.selectbox("Default on file?", ["Y", "N"]),
    "cb_person_cred_hist_length": st.number_input("Credit History Length", 1, 50),
}

loan_intent = st.selectbox("Loan Intent", [
    "EDUCATION", "HOMEIMPROVEMENT", "MEDICAL", "PERSONAL", "VENTURE"
])
for intent in ["EDUCATION", "HOMEIMPROVEMENT", "MEDICAL", "PERSONAL", "VENTURE"]:
    inputs[f"loan_intent_{intent}"] = 1 if loan_intent == intent else 0

inputs["model"] = model

def format_confidence(prob: Union[float, str, None]) -> str:
    if prob is None:
        return "Not Available"
    try:
        if isinstance(prob, str):
            if prob.lower() in ['n/a', 'na', 'nan']:
                return "Not Available"
            prob = float(prob)
        return f"{prob*100:.1f}%"
    except (ValueError, TypeError):
        return "Invalid Value"

if st.button("Predict"):
    try:
        response = requests.post(url, json=inputs, timeout=60)
        response.raise_for_status()
        result = response.json() 
        
        raw_prob = result.get("probability", None)
        st.write(f"Raw probability value: {raw_prob}")
        st.write(f"Type: {type(raw_prob)}")
        
        try:
            prob = float(raw_prob)
        except (TypeError, ValueError):
            st.error("Invalid probability returned from backend.")
            st.stop()

        threshold = 0.5  # default fallback
        if model == "dt":
            threshold = 0.80
        elif model == "xgboost":
            threshold = 0.7354
        elif model == "nn":
            threshold = 0.5625
        elif model== "random forest":
            threshold=0.3660
        final_prediction = 1 if prob >= threshold else 0
        confidence = format_confidence(prob)

        if final_prediction == 1:
            st.success("✅ Approved")
        else:
            st.success("❌ Rejected")

        st.write(f"Confidence: {confidence} (Threshold: {threshold})")

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
