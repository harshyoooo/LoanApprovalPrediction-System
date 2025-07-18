# loan_api_app/serializers.py

from rest_framework import serializers

class LoanInputSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    features = serializers.ListField(
        child=serializers.FloatField(),
        min_length=22,
        max_length=22
    )
