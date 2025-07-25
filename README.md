# 🏦 Loan Approval Prediction System

A complete Machine Learning web application that predicts loan approval based on applicant details. The system includes:

- ✅ Django REST Framework (DRF) backend with REST API
- ✅ Streamlit-based frontend (📍 **[Live Demo Here](https://loanapprovalprediction-system-vymdvxm7fhwsrpo2cjuq6s.streamlit.app/)**)
- ✅ Models trained on Kaggle's [Playground Series - S4E10](https://www.kaggle.com/competitions/playground-series-s4e10) dataset
- ✅ Support for Decision Tree, Random Forest, XGBoost, and Neural Network
- ✅ Production-grade preprocessing pipeline

---

## 🚀 Tech Stack

| Layer      | Tech Stack                     |
|------------|--------------------------------|
| Frontend   | Streamlit                      |
| Backend    | Django + Django REST Framework |
| ML Models  | scikit-learn, XGBoost, Keras   |
| Deployment | Render / Localhost             |

---

## 🧠 Trained Models

All models are trained using **Stratified K-Fold Cross Validation** on the [Playground S4E10 dataset](https://www.kaggle.com/competitions/playground-series-s4e10).

| Model           | AUC Score |
|------------------|-----------|
| Random Forest    | ~ 0.9329  |
| Decision Tree    | ~0.9102   |
| XGBoost          | ~ 0.9533  |
| Neural Network   | ~0.8180   |

---

## Samples