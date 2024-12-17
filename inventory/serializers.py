from rest_framework import serializers

from suppliers.models import Suppliers
from .models import RawMaterials, RawMaterialsLine, FinishedProducts, Image
from warehouse.models import Location
from cloudinary.uploader import upload
from rest_framework.exceptions import ValidationError


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'rack', 'bin_number', 'description', 'quantity', 'is_deleted', 'is_fulled']
        ref_name = 'WarehouseLocation'



class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = ['url']

    def get_url(self, obj):
        """
        Trả về URL dưới dạng chuỗi (JSON serializable).
        """
        if not obj.url:
            return None
        return str(obj.url)  # Chuyển `CloudinaryResource` thành chuỗi


class RawMaterialsLineSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    supplier_id = serializers.IntegerField(write_only=True)  
    supplier_name = serializers.CharField(source='supplier.name', read_only=True) 
    raw_material_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RawMaterialsLine
        fields = [
            'id', 'quantity', 'supplier_id', 'supplier_name', 
            'price_per_unit', 'line_total', 'location',
            'created_at', 'is_deleted', 'is_available', 'raw_material_id'
        ]
        read_only_fields = ['line_total', 'created_at']

    def create(self, validated_data):
        """
        Custom create method để xử lý nested location, supplier_id và raw_material_id.
        """
        location_data = validated_data.pop('location', None)
        raw_material_id = validated_data.pop('raw_material_id', None)
        supplier_id = validated_data.pop('supplier_id', None)

        # Xử lý location
        if location_data:
            location, created = Location.objects.get_or_create(**location_data)
            validated_data['location'] = location

        # Liên kết RawMaterial
        try:
            raw_material = RawMaterials.objects.get(id=raw_material_id)
            validated_data['raw_material'] = raw_material
        except RawMaterials.DoesNotExist:
            raise serializers.ValidationError({"raw_material_id": "Invalid raw_material_id"})

        # Liên kết Supplier
        try:
            supplier = Suppliers.objects.get(id=supplier_id)
            validated_data['supplier'] = supplier
        except Suppliers.DoesNotExist:
            raise serializers.ValidationError({"supplier_id": "Invalid supplier_id"})

        # Tạo đối tượng RawMaterialsLine
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Custom update method để xử lý nested location, supplier_id và raw_material_id.
        """
        location_data = validated_data.pop('location', None)
        raw_material_id = validated_data.pop('raw_material_id', None)
        supplier_id = validated_data.pop('supplier_id', None)

        # Xử lý location
        if location_data:
            location = instance.location
            if location:  # Nếu location đã tồn tại, cập nhật
                for attr, value in location_data.items():
                    setattr(location, attr, value)
                location.save()
            else:  # Nếu chưa có location, tạo mới
                location = Location.objects.create(**location_data)
                instance.location = location

        # Liên kết RawMaterial
        if raw_material_id:
            try:
                raw_material = RawMaterials.objects.get(id=raw_material_id)
                instance.raw_material = raw_material
            except RawMaterials.DoesNotExist:
                raise serializers.ValidationError({"raw_material_id": "Invalid raw_material_id"})

        # Liên kết Supplier
        if supplier_id:
            try:
                supplier = Suppliers.objects.get(id=supplier_id)
                instance.supplier = supplier
            except Suppliers.DoesNotExist:
                raise serializers.ValidationError({"supplier_id": "Invalid supplier_id"})

        # Cập nhật các trường còn lại
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class RawMaterialsSerializer(serializers.ModelSerializer):
    raw_materials_lines = RawMaterialsLineSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)  # Trả về danh sách URL ảnh
    uploaded_images = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )

    class Meta:
        model = RawMaterials
        fields = [
            'id', 'name', 'category', 'description', 'total_quantity',
            'total_amount', 'created_at', 'updated_at', 'is_available',
            'is_deleted', 'raw_materials_lines', 'images', 'uploaded_images'
        ]
        read_only_fields = ['total_quantity', 'total_amount', 'created_at', 'updated_at']

    def get_image_urls(self, obj):
        """Trả về danh sách URL ảnh từ bảng Image"""
        return [image.url for image in obj.images.all()]

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        raw_material = RawMaterials.objects.create(**validated_data)

        for image in images:
            try:
                upload_result = upload(image)  # Upload lên Cloudinary
                Image.objects.create(
                    raw_material=raw_material,
                    url=upload_result.get('secure_url')
                )
            except Exception as e:
                raise serializers.ValidationError(f"Failed to upload image: {str(e)}")

        return raw_material

    def update(self, instance, validated_data):
        images = validated_data.pop('images', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for image in images:
            try:
                upload_result = upload(image)
                Image.objects.create(
                    raw_material=instance,
                    url=upload_result.get('secure_url')
                )
            except Exception as e:
                raise serializers.ValidationError(f"Failed to upload image: {str(e)}")

        return instance

class FinishedProductsSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    images = ImageSerializer(many=True, read_only=True)  # Trả về danh sách URL ảnh
    uploaded_images = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )  # Xử lý upload ảnh từ client

    class Meta:
        model = FinishedProducts
        fields = [
            'id', 'name', 'category', 'selling_price', 'total_quantity',
            'unit', 'location', 'description', 'expired_date',
            'is_available', 'is_deleted', 'created_at', 'updated_at', 'images', 'uploaded_images'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        """
        Tạo mới FinishedProducts và xử lý upload images lên Cloudinary.
        """
        uploaded_images = validated_data.pop('uploaded_images', [])  # Lấy danh sách ảnh upload
        location_data = validated_data.pop('location', None)
        total_quantity = validated_data.get('total_quantity')  # Lấy giá trị total_quantity

        # Xử lý location nếu có
        if location_data:
            location_data['quantity'] = total_quantity
            location, created = Location.objects.get_or_create(**location_data)
            validated_data['location'] = location

        finished_product = FinishedProducts.objects.create(**validated_data)

        # Upload ảnh lên Cloudinary và lưu vào database
        for image in uploaded_images:
            try:
                upload_result = upload(image)
                Image.objects.create(
                    finished_product=finished_product,
                    url=upload_result.get('secure_url')
                )
            except Exception as e:
                raise serializers.ValidationError(f"Failed to upload image: {str(e)}")

        return finished_product

    def update(self, instance, validated_data):
        """
        Cập nhật FinishedProducts và xử lý upload images lên Cloudinary.
        """
        uploaded_images = validated_data.pop('uploaded_images', [])  # Lấy danh sách ảnh upload
        location_data = validated_data.pop('location', None)
        total_quantity = validated_data.get('total_quantity')  # Lấy giá trị total_quantity
        # Xử lý location nếu có
        if location_data:
            location = instance.location
            if location:
                location.quantity = total_quantity
                for attr, value in location_data.items():
                    setattr(location, attr, value)
                location.save()
            else:
                # Tạo mới location nếu chưa có
                location_data['quantity'] = total_quantity
                location = Location.objects.create(**location_data)
                instance.location = location

        # Cập nhật các trường thông tin khác
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Upload ảnh mới lên Cloudinary và lưu vào database
        for image in uploaded_images:
            try:
                upload_result = upload(image)
                Image.objects.create(
                    finished_product=instance,
                    url=upload_result.get('secure_url')
                )
            except Exception as e:
                raise serializers.ValidationError(f"Failed to upload image: {str(e)}")

        return instance
    