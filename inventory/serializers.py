from rest_framework import serializers
from .models import RawMaterials, RawMaterialsLine, FinishedProducts, Image
from warehouse.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'rack', 'bin_number', 'description', 'quantity', 'is_deleted', 'is_fulled']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'url']


class RawMaterialsLineSerializer(serializers.ModelSerializer):
    location = LocationSerializer
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    class Meta:
        model = RawMaterialsLine
        fields = [
            'id', 'quantity', 'supplier', 'supplier_name', 
            'price_per_unit', 'line_total', 'location', 
            'created_at', 'is_deleted', 'is_available'
        ]
        read_only_fields = ['line_total', 'created_at']

    def create(self, validated_data):
        """
        Custom create method để xử lý nested location.
        """
        location_data = validated_data.pop('location')  
        location, created = Location.objects.get_or_create(**location_data)
        validated_data['location'] = location  
        return super().create(validated_data)

class RawMaterialsSerializer(serializers.ModelSerializer):
    raw_materials_lines = RawMaterialsLineSerializer(many=True, read_only=True)  # Nested RawMaterialsLine
    images = ImageSerializer(many=True, read_only=True, source='images')  # Nested images

    class Meta:
        model = RawMaterials
        fields = [
            'id', 'name', 'category', 'description', 'total_quantity', 
            'total_amount', 'created_at', 'updated_at', 'is_available', 
            'is_deleted', 'raw_materials_lines', 'images'
        ]
        read_only_fields = ['total_quantity', 'total_amount', 'created_at', 'updated_at']


class FinishedProductsSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)  # Nested LocationSerializer
    images = ImageSerializer(many=True, read_only=True, source='images')  # Nested images

    class Meta:
        model = FinishedProducts
        fields = [
            'id', 'name', 'category', 'selling_price', 'total_quantity', 
            'unit', 'location', 'description', 'expired_date', 
            'is_available', 'is_deleted', 'created_at', 'updated_at', 'images'
        ]
        read_only_fields = ['created_at', 'updated_at']
