from rest_framework import serializers
from .models import Suppliers, Representative


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = [
            'id', 'representative', 'avatar', 'name', 'address', 'tel', 'email',
            'tax_code', 'bank_name', 'bank_branch', 'bank_number', 'swift_code', 'created_at'
        ]
        read_only_fields = ['representative']  # Không ghi trực tiếp vào trường này

class RepresentativeSerializer(serializers.ModelSerializer):
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Suppliers.objects.all(), write_only=True
    )  # Nhận ID của Supplier khi tạo Representative

    class Meta:
        model = Representative
        fields = [
            'id', 'avatar', 'name', 'birth', 'gender', 'tel', 'email', 'position',
            'bank_name', 'bank_branch', 'bank_number', 'swift_code', 'supplier_id'
        ]

    def create(self, validated_data):
        # Lấy Supplier từ supplier_id
        supplier = validated_data.pop('supplier_id')
        representative = Representative.objects.create(**validated_data)
        supplier.representative = representative  # Liên kết với Supplier
        supplier.save()
        return representative
