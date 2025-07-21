import streamlit as st
import pandas as pd
import requests

# Exact column order expected by your model
expected_columns = [
    'person_age', 'person_income', 'person_emp_length', 'loan_amnt', 'loan_int_rate',
    'loan_percent_income', 'cb_person_cred_hist_length',

    # One-hot encoded: Home ownership
    'person_home_ownership_OTHER', 'person_home_ownership_OWN', 'person_home_ownership_RENT',

    # One-hot encoded: Loan intent
    'loan_intent_EDUCATION', 'loan_intent_HOMEIMPROVEMENT', 'loan_intent_MEDICAL',
    'loan_intent_PERSONAL', 'loan_intent_VENTURE',

    # One-hot encoded: Loan grade
    'loan_grade_B', 'loan_grade_C', 'loan_grade_D', 'loan_grade_E',
    'loan_grade_F', 'loan_grade_G',

    # One-hot encoded: Default history
    'cb_person_default_on_file_Y'
]

# UI
st.title("Loan Approval Predictor")
st.markdown("Fill in details to predict approval")

# Model selector
model_name = st.selectbox("Select Model", ["decision_tree", "neural_net", "xgboost"])

# Inputs
person_age = st.number_input("Age", min_value=18, max_value=100, value=25)
person_income = st.number_input("Annual Income", min_value=0, value=50000)
person_emp_length = st.number_input("Employment Length (years)", min_value=0.0, max_value=50.0, value=2.0)
loan_amnt = st.number_input("Loan Amount", min_value=1000, value=10000)
loan_int_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=40.0, value=10.0)
loan_percent_income = loan_amnt / person_income if person_income > 0 else 0.0
cb_person_cred_hist_length = st.number_input("Credit History Length", min_value=0, value=3)

# Categorical
home_ownership = st.selectbox("Home Ownership", ["OTHER", "OWN", "RENT"])
loan_intent = st.selectbox("Loan Intent", ["EDUCATION", "HOMEIMPROVEMENT", "MEDICAL", "PERSONAL", "VENTURE"])
loan_grade = st.selectbox("Loan Grade", ["B", "C", "D", "E", "F", "G"])
default_history = st.selectbox("Any Past Default?", ["No", "Yes"])

if st.button("Predict"):
    input_data = {
        'person_age': person_age,
        'person_income': person_income,
        'person_emp_length': person_emp_length,
        'loan_amnt': loan_amnt,
        'loan_int_rate': loan_int_rate,
        'loan_percent_income': loan_percent_income,
        'cb_person_cred_hist_length': cb_person_cred_hist_length,
    }

    for val in ["OTHER", "OWN", "RENT"]:
        input_data[f"person_home_ownership_{val}"] = 1 if home_ownership == val else 0

    for val in ["EDUCATION", "HOMEIMPROVEMENT", "MEDICAL", "PERSONAL", "VENTURE"]:
        input_data[f"loan_intent_{val}"] = 1 if loan_intent == val else 0

    for val in ["B", "C", "D", "E", "F", "G"]:
        input_data[f"loan_grade_{val}"] = 1 if loan_grade == val else 0

    input_data["cb_person_default_on_file_Y"] = 1 if default_history == "Yes" else 0

    # Ensure proper column order
    final_input = [int(input_data[col]) if isinstance(input_data[col], bool) else input_data[col] for col in expected_columns]

    try:
        response = requests.post(
            "https://loanapprovalprediction-system.onrender.com/api/predict/",
            json={
                "model_name": model_name,
                "features": final_input
            }
        )
        prediction = response.json().get("prediction", "Error")
        st.success(f"✅ Prediction: {prediction}")
    except Exception as e:
        st.error(f"❌ Could not contact backend: {e}")
