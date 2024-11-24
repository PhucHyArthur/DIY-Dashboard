from rest_framework import serializers
from .models import RawMaterials, FinishedProducts
from warehouse.models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'rack', 'bin_number', 'description', 'quantity', 'is_delete', 'is_fulled']

class RawMaterialsSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = RawMaterials
        fields = ['id', 'name', 'category', 'image', 'price_per_unit', 'unit', 'quantity_in_stock', 'location', 'description', 'expired_date', 'is_available', 'is_deleted']

class FinishedProductsSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = FinishedProducts
        fields = ['id', 'name', 'category', 'selling_price', 'quantity_in_stock', 'location', 'description', 'expired_date', 'main_image', 'sub_image_1', 'sub_image_2', 'is_available', 'is_deleted']
