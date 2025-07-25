import pandas as pd
def feature_engineering(df):
    eps = 1e-6
    df['loan_to_income_ratio'] = df['loan_amnt'] / (df['person_income'] +eps) 
    df['financial_burden'] = df['loan_amnt'] * df['loan_int_rate'] 
    df['income_per_year_emp'] = df['person_income'] / (df['person_emp_length']+eps)
    df['cred_hist_to_age_ratio'] = df['cb_person_cred_hist_length'] / (df['person_age']+eps)
    df['int_to_loan_ratio'] = df['loan_int_rate'] / (df['loan_amnt']+eps)
    df['loan_int_emp_interaction'] = df['loan_int_rate'] * df['person_emp_length']
    df['debt_to_credit_ratio'] = df['loan_amnt'] / (df['cb_person_cred_hist_length']+eps) 
    df['int_to_cred_hist'] = df['loan_int_rate'] / (df['cb_person_cred_hist_length']+eps)  
    df['int_per_year_emp'] = df['loan_int_rate'] / (df['person_emp_length']+eps)
    df['loan_amt_per_emp_year'] = df['loan_amnt'] / (df['person_emp_length']+ eps)      
    df['income_to_loan_ratio'] = df['person_income'] / (df['loan_amnt'] +eps) 
    return df

def preprocess_input(data: dict):
    df = pd.DataFrame([data])

    # Categorical mapping
    ownership_map = {"RENT": 0, "OWN": 1, "MORTGAGE": 2, "OTHER": 3}
    default_map = {"Y": 1, "N": 0}
    grade_map = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}

    df['person_home_ownership'] = df['person_home_ownership'].map(ownership_map)
    df['cb_person_default_on_file'] = df['cb_person_default_on_file'].map(default_map)
    df['loan_grade'] = df['loan_grade'].map(grade_map)

    # Add one-hot loan intent columns if not present
    for col in ['loan_intent_EDUCATION', 'loan_intent_HOMEIMPROVEMENT',
                'loan_intent_MEDICAL', 'loan_intent_PERSONAL', 'loan_intent_VENTURE']:
        if col not in df.columns:
            df[col] = 0

    # ✅ Call feature_engineering here
    df = feature_engineering(df)
    return df