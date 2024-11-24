from rest_framework import serializers
from .models import SalesOrder, SalesOrderLine, PurchaseOrder, PurchaseOrderLine
from inventory.models import FinishedProducts, RawMaterials
from users.models import Clients
from suppliers.models import Suppliers

class FinishedProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishedProducts
        fields = ['id', 'name', 'category', 'selling_price', 'quantity_in_stock', 'location', 'description', 'expired_date', 'main_image', 'sub_image_1', 'sub_image_2', 'is_available', 'is_deleted']

class RawMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterials
        fields = ['id', 'name', 'category', 'image', 'price_per_unit', 'unit', 'quantity_in_stock', 'location', 'description', 'expired_date', 'is_available', 'is_deleted']

class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ['id', 'name', 'email', 'phone', 'address']

class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ['id', 'name', 'contact_name', 'contact_email', 'phone', 'address']

class SalesOrderLineSerializer(serializers.ModelSerializer):
    product = FinishedProductsSerializer()

    class Meta:
        model = SalesOrderLine
        fields = ['id', 'sales_order', 'product', 'quantity', 'unit_price', 'line_total', 'created_at']

class SalesOrderSerializer(serializers.ModelSerializer):
    order_lines = SalesOrderLineSerializer(many=True)
    client = ClientsSerializer()

    class Meta:
        model = SalesOrder
        fields = ['id', 'order_number', 'client', 'order_date', 'due_date', 'status', 'total_amount', 'remarks', 'is_deleted', 'created_at', 'order_lines']

class PurchaseOrderLineSerializer(serializers.ModelSerializer):
    material = RawMaterialsSerializer()

    class Meta:
        model = PurchaseOrderLine
        fields = ['id', 'purchase_order', 'material', 'quantity', 'unit_price', 'line_total', 'created_at']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    order_lines = PurchaseOrderLineSerializer(many=True)
    supplier = SuppliersSerializer()

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'order_number', 'supplier', 'order_date', 'due_date', 'status', 'total_amount', 'remarks', 'is_deleted', 'created_at', 'order_lines']
