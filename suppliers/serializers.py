from rest_framework import serializers
from .models import Representative, Suppliers

class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representative
        fields = ['id', 'avatar', 'name', 'birth', 'gender', 'tel', 'email', 'position', 'bank_name', 'bank_branch', 'bank_number', 'swift_code', 'created_at']

class SuppliersSerializer(serializers.ModelSerializer):
    representative = RepresentativeSerializer()

    class Meta:
        model = Suppliers
        fields = ['id', 'representative', 'avatar', 'name', 'address', 'tel', 'email', 'tax_code', 'bank_name', 'bank_branch', 'bank_number', 'swift_code', 'created_at']
