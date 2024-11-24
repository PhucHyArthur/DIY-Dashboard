from rest_framework import serializers
from inventory.models import FinishedProducts
from .models import Cart, Cart_Line, Favorites, Favorite_Line

class FinishedProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishedProducts
        fields = ['id', 'name', 'category', 'selling_price', 'quantity_in_stock', 'location', 'description', 'expired_date', 'main_image', 'sub_image_1', 'sub_image_2', 'is_available', 'is_deleted']

class CartLineSerializer(serializers.ModelSerializer):
    product = FinishedProductsSerializer()

    class Meta:
        model = Cart_Line
        fields = ['id', 'cart', 'product', 'quantity', 'unit_price', 'line_total']

class CartSerializer(serializers.ModelSerializer):
    cart_lines = CartLineSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'is_active', 'created_at', 'updated_at', 'cart_lines']

class FavoriteLineSerializer(serializers.ModelSerializer):
    product = FinishedProductsSerializer()

    class Meta:
        model = Favorite_Line
        fields = ['id', 'favorites', 'product', 'added_at']

class FavoritesSerializer(serializers.ModelSerializer):
    favorite_lines = FavoriteLineSerializer(many=True)

    class Meta:
        model = Favorites
        fields = ['id', 'user', 'created_at', 'favorite_lines']
