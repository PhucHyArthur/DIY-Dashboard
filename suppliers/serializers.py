from rest_framework import serializers
from .models import Suppliers, Representative

class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representative
        fields = ['id', 'avatar', 'name', 'birth', 'gender', 'tel', 'email', 'position', 'bank_name', 'bank_branch', 'bank_number', 'swift_code']

class SuppliersSerializer(serializers.ModelSerializer):
    representative = RepresentativeSerializer()  # Nested serializer

    class Meta:
        model = Suppliers
        fields = ['id', 'representative', 'avatar', 'name', 'address', 'tel', 'email', 'tax_code', 
                  'bank_name', 'bank_branch', 'bank_number', 'swift_code', 'created_at']

    def create(self, validated_data):
        # Tách dữ liệu của representative
        representative_data = validated_data.pop('representative', None)

        # Tạo mới Suppliers
        supplier = Suppliers.objects.create(**validated_data)

        # Tạo mới hoặc liên kết representative nếu có
        if representative_data:
            representative = Representative.objects.create(**representative_data)
            supplier.representative = representative
            supplier.save()

        return supplier

    def update(self, instance, validated_data):
        # Lấy và xử lý dữ liệu cho representative
        representative_data = validated_data.pop('representative', None)

        # Cập nhật các trường của Suppliers
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Nếu có thông tin representative, cập nhật hoặc tạo mới
        if representative_data:
            representative = instance.representative
            representative_serializer = RepresentativeSerializer(representative, data=representative_data)
            if representative_serializer.is_valid():
                representative_serializer.save()  # Cập nhật representative
            else:
                raise serializers.ValidationError(representative_serializer.errors)

        instance.save()
        return instance