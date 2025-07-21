# loan_api_app/views.py

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoanInputSerializer

import joblib
import os
import numpy as np
import traceback  # ✅ Added for detailed error logs
from django.http import JsonResponse

def home(request):
    return JsonResponse({'status': 'API is live'})

class LoanApprovalPrediction(APIView):
    def post(self, request):
        serializer = LoanInputSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            model_name = data["model_name"]
            features = data["features"]

            # ✅ Log incoming data
            print(f"[INFO] Received model: {model_name}, features length: {len(features)}")

            model_path = os.path.join(os.path.dirname(__file__), "models", f"{model_name}_model1.pkl")

            try:
                # ✅ Load model
                model = joblib.load(model_path)
                print(f"[INFO] Model loaded successfully: {model_name}")
            except Exception as e:
                error_trace = traceback.format_exc()
                print(f"[ERROR] Model loading failed:\n{error_trace}")
                return Response({"error": f"Could not load model: {str(e)}"}, status=500)

            try:
                input_data = np.array([features])  # Already preprocessed by frontend
                prediction = model.predict(input_data)[0]
                print(f"[INFO] Prediction done: {prediction}")
                return Response({"prediction": int(prediction)})
            except Exception as e:
                error_trace = traceback.format_exc()
                print(f"[ERROR] Prediction failed:\n{error_trace}")
                return Response({"error": f"Prediction error: {str(e)}"}, status=500)

        else:
            print(f"[ERROR] Serializer error: {serializer.errors}")
            return Response(serializer.errors, status=400)
