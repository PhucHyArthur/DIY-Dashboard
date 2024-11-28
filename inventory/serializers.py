from rest_framework import serializers
from .models import RawMaterials, FinishedProducts
from warehouse.models import Location
from rest_framework.exceptions import ValidationError
import base64
from firebase_admin import storage
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
        
        images = validated_data.pop('image', [])    
        validated_data['image'] = self._process_images(images)

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
    
    def _process_images(self, images, existing_images=[]):
        """
        Xử lý danh sách ảnh: nếu là base64 thì upload lên Firebase và trả về URL,
        nếu là URL thì giữ nguyên.
        """
        processed_images = list(existing_images)
        for image in images:
            if self._is_base64(image):
                url = self._upload_to_firebase(image)
                processed_images.append(url)
            elif self._is_url(image):
                processed_images.append(image)
            else:
                raise ValidationError({"image": "Invalid image format. Provide a valid URL or Base64 string."})
        return processed_images
    
    def _is_base64(self, data):
        """Kiểm tra xem chuỗi có phải là Base64 hay không."""
        try:
            base64.b64decode(data)
            return True
        except Exception:
            return False
        
    def _is_url(self, url):
        """Kiểm tra xem chuỗi có phải là URL hay không."""
        return url.startswith('http://') or url.startswith('https://')

    def _upload_to_firebase(self, base64_data):
        """Upload file từ base64 lên Firebase và trả về URL."""
        bucket = storage.bucket()
        file_name = f"images/{uuid.uuid4()}.png"
        blob = bucket.blob(file_name)
        blob.upload_from_string(base64.b64decode(base64_data), content_type='image/png')
        blob.make_public()
        return blob.public_url
