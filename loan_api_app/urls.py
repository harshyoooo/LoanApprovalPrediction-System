# loan_api_app/urls.py

from django.urls import path
from .views import LoanApprovalPrediction

urlpatterns = [
    path('predict/', LoanApprovalPrediction.as_view(), name='loan-predict'),
]
