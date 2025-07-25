from rest_framework.views import APIView
from rest_framework.response import Response
import joblib
import os
from .preprocessing import preprocess_input

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_FILE_MAP = {
    "random forest": "rf_model5.pkl",
    "dt":"dt_model5.pkl",
    "nn": "model_NN5.pkl",
    "xgboost": "xgb_model5.pkl",
}

class PredictAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            model_type = data.get("model") 

            if not model_type or model_type not in MODEL_FILE_MAP:
                return Response({"error": "Invalid or missing model type"}, status=400)

            model_filename = MODEL_FILE_MAP[model_type]
            model_path = os.path.join(BASE_DIR, "models", model_filename)

            if not os.path.exists(model_path):
                return Response({"error": f"Model file not found: {model_filename}"}, status=404)

            model = joblib.load(model_path)

            input_data = {k: v for k, v in data.items() if k != "model"}
            preprocessed = preprocess_input(input_data)

            prediction = model.predict(preprocessed)[0]

            if hasattr(model, "predict_proba"):
                prob = model.predict_proba(preprocessed)[0][int(prediction)]
            else:
                prob = None

            return Response({
                "prediction": int(prediction),
                "probability": round(float(prob), 3) if prob is not None else "N/A"
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
