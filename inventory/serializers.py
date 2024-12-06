from rest_framework import serializers
from .models import RawMaterials, FinishedProducts, Image
from warehouse.models import Location

# Serializer cho Image
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'url']

# Serializer cho Location
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'rack', 'bin_number', 'description', 'quantity', 'is_deleted', 'is_fulled']

# Serializer cho RawMaterials
class RawMaterialsSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    images = ImageSerializer(many=True, required=False)  # Nested Serializer cho ảnh

    class Meta:
        model = RawMaterials
        fields = [
            'id', 'name', 'category', 'images', 'price_per_unit', 'unit',
            'quantity_in_stock', 'location', 'description', 'expired_date',
            'is_available', 'is_deleted'
        ]

    def create(self, validated_data):
        # Xử lý tạo Location trước khi tạo RawMaterials
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)

        # Lấy dữ liệu ảnh
        images_data = validated_data.pop('images', [])
        
        # Tạo RawMaterials
        raw_material = RawMaterials.objects.create(location=location, **validated_data)

        # Tạo các đối tượng Image liên quan
        for image_data in images_data:
            Image.objects.create(raw_material=raw_material, **image_data)

        return raw_material

    def update(self, instance, validated_data):
        # Cập nhật Location nếu có thay đổi
        location_data = validated_data.pop('location', None)
        if location_data:
            for attr, value in location_data.items():
                setattr(instance.location, attr, value)
            instance.location.save()

        # Xóa và cập nhật lại ảnh liên quan
        images_data = validated_data.pop('images', [])
        instance.images.all().delete()  # Xóa ảnh cũ
        for image_data in images_data:
            Image.objects.create(raw_material=instance, **image_data)

        # Cập nhật các trường của RawMaterials
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# Serializer cho FinishedProducts
class FinishedProductsSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    images = ImageSerializer(many=True, required=False)  # Nested Serializer cho ảnh

    class Meta:
        model = FinishedProducts
        fields = [
            'id', 'name', 'category', 'selling_price', 'unit', 'quantity_in_stock',
            'location', 'description', 'expired_date', 'images', 'is_available', 'is_deleted'
        ]

    def create(self, validated_data):
        # Xử lý tạo Location trước khi tạo FinishedProducts
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)

        # Lấy dữ liệu ảnh
        images_data = validated_data.pop('images', [])
        
        # Tạo FinishedProducts
        finished_product = FinishedProducts.objects.create(location=location, **validated_data)

        # Tạo các đối tượng Image liên quan
        for image_data in images_data:
            Image.objects.create(finished_product=finished_product, **image_data)

        return finished_product

    def update(self, instance, validated_data):
        # Cập nhật Location nếu có thay đổi
        location_data = validated_data.pop('location', None)
        if location_data:
            for attr, value in location_data.items():
                setattr(instance.location, attr, value)
            instance.location.save()

        # Xóa và cập nhật lại ảnh liên quan
        images_data = validated_data.pop('images', [])
        instance.images.all().delete()  # Xóa ảnh cũ
        for image_data in images_data:
            Image.objects.create(finished_product=instance, **image_data)

        # Cập nhật các trường của FinishedProducts
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
