from rest_framework import serializers
from .models import RawMaterials, FinishedProducts
from warehouse.models import Location
from rest_framework.exceptions import ValidationError
import base64
import uuid 

# Serializer cho Location
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'rack', 'bin_number', 'description', 'quantity', 'is_deleted', 'is_fulled']

# Serializer cho RawMaterials
class RawMaterialsSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = RawMaterials
        fields = ['id', 'name', 'category', 'image', 'price_per_unit', 'unit', 'quantity_in_stock', 'location', 'description', 'expired_date', 'is_available', 'is_deleted']

    def create(self, validated_data):
        # Xử lý tạo Location trước khi tạo RawMaterials
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)

        # Tạo RawMaterials
        raw_material = RawMaterials.objects.create(location=location, **validated_data)
        return raw_material

    def update(self, instance, validated_data):
        # Cập nhật Location nếu có thay đổi
        location_data = validated_data.pop('location', None)
        if location_data:
            # Cập nhật Location
            for attr, value in location_data.items():
                setattr(instance.location, attr, value)
            instance.location.save()

        # Cập nhật RawMaterials
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# Serializer cho FinishedProducts
class FinishedProductsSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = FinishedProducts
        fields = ['id', 'name', 'category', 'selling_price',"unit", 'quantity_in_stock', 'location', 'description', 'expired_date', 'image', 'is_available', 'is_deleted']

    def create(self, validated_data):
        # Xử lý tạo Location trước khi tạo FinishedProducts
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)

        # Tạo FinishedProducts
        finished_product = FinishedProducts.objects.create(location=location, **validated_data)
        return finished_product

    def update(self, instance, validated_data):
        # Cập nhật Location nếu có thay đổi
        location_data = validated_data.pop('location', None)
        if location_data:
            # Cập nhật Location
            for attr, value in location_data.items():
                setattr(instance.location, attr, value)
            instance.location.save()

        # Cập nhật FinishedProducts
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
