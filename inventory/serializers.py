from rest_framework import serializers

from suppliers.models import Suppliers
from .models import RawMaterials, RawMaterialsLine, FinishedProducts, Image
from warehouse.models import Rack
from cloudinary.uploader import upload

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
    rack = serializers.PrimaryKeyRelatedField(queryset=Rack.objects.all(), required=False)
    supplier_id = serializers.IntegerField(write_only=True)  
    supplier_name = serializers.CharField(source='supplier.name', read_only=True) 
    raw_material_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RawMaterialsLine
        fields = [
            'id', 'quantity', 'supplier_id', 'supplier_name', 
            'price_per_unit', 'line_total', 'rack', 'bin_number', 'unit',
            'created_at', 'is_deleted', 'is_available', 'raw_material_id'
        ]
        read_only_fields = ['line_total', 'created_at']

    def create(self, validated_data):
        """
        Custom create method để xử lý nested location, supplier_id và raw_material_id.
        """
        raw_material_id = validated_data.pop('raw_material_id', None)
        supplier_id = validated_data.pop('supplier_id', None)

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
        raw_material_id = validated_data.pop('raw_material_id', None)
        supplier_id = validated_data.pop('supplier_id', None)

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
    rack = serializers.PrimaryKeyRelatedField(queryset=Rack.objects.all(), required=False)
    images = ImageSerializer(many=True, read_only=True)  # Trả về danh sách URL ảnh
    uploaded_images = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )

    class Meta:
        model = FinishedProducts
        fields = [
            'id', 'name', 'category', 'selling_price', 'total_quantity',
            'unit', 'rack', 'bin_number', 'description', 'expired_date',
            'is_available', 'is_deleted', 'created_at', 'updated_at',
            'images', 'uploaded_images'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_image_urls(self, obj):
        """Trả về danh sách URL ảnh từ bảng Image"""
        return [image.url for image in obj.images.all()]

    def create(self, validated_data):
        """
        Tạo mới sản phẩm và upload các ảnh từ uploaded_images.
        """
        uploaded_images = validated_data.pop('uploaded_images', [])  # Lấy danh sách ảnh

        # Tạo mới FinishedProducts
        finished_product = FinishedProducts.objects.create(**validated_data)

        # Upload từng ảnh từ uploaded_images và lưu vào Image model
        for image in uploaded_images:
            try:
                upload_result = upload(image)  # Upload ảnh lên Cloudinary
                Image.objects.create(
                    finished_product=finished_product,
                    url=upload_result.get('secure_url')
                )
            except Exception as e:
                raise serializers.ValidationError(f"Failed to upload image: {str(e)}")

        return finished_product

    def update(self, instance, validated_data):
        """
        Cập nhật sản phẩm và upload các ảnh từ uploaded_images.
        """
        uploaded_images = validated_data.pop('uploaded_images', [])  # Lấy danh sách ảnh

        # Cập nhật các trường thông tin sản phẩm
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Upload từng ảnh từ uploaded_images và lưu vào Image model
        for image in uploaded_images:
            try:
                upload_result = upload(image)  # Upload ảnh lên Cloudinary
                Image.objects.create(
                    finished_product=instance,
                    url=upload_result.get('secure_url')
                )
            except Exception as e:
                raise serializers.ValidationError(f"Failed to upload image: {str(e)}")

        return instance