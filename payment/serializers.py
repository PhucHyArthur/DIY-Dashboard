# payment/serializers.py
from rest_framework import serializers

class PaymentSerializer(serializers.Serializer):
    client_id = serializers.CharField(max_length=100)
    order_id = serializers.CharField(max_length=100)
    amount = serializers.IntegerField(min_value=1)  # Số tiền phải lớn hơn 0
    description = serializers.CharField(max_length=255)
