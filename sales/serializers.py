from rest_framework import serializers
from .models import Cart_Line , Favorite_Line
from inventory.models import FinishedProducts
from users.models import Employee

class CartLineSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart Line model.
    """
    product = serializers.PrimaryKeyRelatedField(queryset=FinishedProducts.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)  # read-only, không cần nhập

    class Meta:
        model = Cart_Line
        fields = ['id', 'user', 'product', 'quantity', 'unit_price', 'line_total']

    def validate(self, data):
        """
        Ensure that the quantity and unit price are valid.
        """
        # Lấy giá bán từ sản phẩm
        product = data.get('product')
        if not product:
            raise serializers.ValidationError("Product is required.")
        
        # Cập nhật unit_price với giá bán của sản phẩm
        data['unit_price'] = product.selling_price

        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")

        return data

    def create(self, validated_data):
        """
        Create a new Cart_Line instance with validated data.
        """
        # Gọi validate trước khi tạo để đảm bảo unit_price được set đúng
        validated_data = self.validate(validated_data)
        
        # Tạo Cart_Line mới
        cart_line = Cart_Line.objects.create(**validated_data)
        return cart_line



class FavoriteLineSerializer(serializers.ModelSerializer):
    """
    Serializer for Favorite Line model.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    class Meta:
        model = Favorite_Line
        fields = ['id', 'user', 'product']
