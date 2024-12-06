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
    location = LocationSerializer()
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
        location_data = validated_data.pop('location', None)
        if location_data:
            location, created = Location.objects.get_or_create(**location_data)
            validated_data['location'] = location
        return super().create(validated_data)


class RawMaterialsSerializer(serializers.ModelSerializer):
    raw_materials_lines = RawMaterialsLineSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True)  # Cho phép chỉnh sửa

    class Meta:
        model = RawMaterials
        fields = [
            'id', 'name', 'category', 'description', 'total_quantity',
            'total_amount', 'created_at', 'updated_at', 'is_available',
            'is_deleted', 'raw_materials_lines', 'images'
        ]
        read_only_fields = ['total_quantity', 'total_amount', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Tạo mới RawMaterials và xử lý nested images.
        """
        images_data = validated_data.pop('images', [])
        raw_material = RawMaterials.objects.create(**validated_data)
        for image_data in images_data:
            Image.objects.create(raw_material=raw_material, **image_data)
        return raw_material

    def update(self, instance, validated_data):
        """
        Cập nhật RawMaterials và xử lý nested images.
        """
        images_data = validated_data.pop('images', [])
        instance = super().update(instance, validated_data)

        # Cập nhật ảnh
        instance.images.all().delete()  # Xóa ảnh cũ
        for image_data in images_data:
            Image.objects.create(raw_material=instance, **image_data)
        return instance


class FinishedProductsSerializer(serializers.ModelSerializer):
    location = LocationSerializer()  # Cho phép chỉnh sửa
    images = ImageSerializer(many=True)  # Cho phép chỉnh sửa ảnh

    class Meta:
        model = FinishedProducts
        fields = [
            'id', 'name', 'category', 'selling_price', 'total_quantity',
            'unit', 'location', 'description', 'expired_date',
            'is_available', 'is_deleted', 'created_at', 'updated_at', 'images'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        """
        Tạo mới FinishedProducts và xử lý nested images.
        """
        images_data = validated_data.pop('images', [])
        location_data = validated_data.pop('location', None)
        if location_data:
            location, created = Location.objects.get_or_create(**location_data)
            validated_data['location'] = location

        finished_product = FinishedProducts.objects.create(**validated_data)
        for image_data in images_data:
            Image.objects.create(finished_product=finished_product, **image_data)
        return finished_product

    def update(self, instance, validated_data):
        """
        Cập nhật FinishedProducts và xử lý nested images.
        """
        images_data = validated_data.pop('images', [])
        location_data = validated_data.pop('location', None)

        if location_data:
            location, created = Location.objects.get_or_create(**location_data)
            validated_data['location'] = location

        instance = super().update(instance, validated_data)

        # Cập nhật ảnh
        instance.images.all().delete()
        for image_data in images_data:
            Image.objects.create(finished_product=instance, **image_data)
        return instance
