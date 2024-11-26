from rest_framework import serializers
from .models import SalesOrder, SalesOrderLine, PurchaseOrder, PurchaseOrderLine
from inventory.models import FinishedProducts, RawMaterials
from users.models import Customer
from suppliers.models import Suppliers

class SalesOrderSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())  # Customer ID

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'order_number', 'client', 'order_date', 'due_date', 
            'status', 'total_amount', 'remarks', 'is_deleted', 'created_at'
        ]


class SalesOrderLineSerializer(serializers.ModelSerializer):
    sales_order = serializers.PrimaryKeyRelatedField(queryset=SalesOrder.objects.all())  # Sales Order ID
    product = serializers.PrimaryKeyRelatedField(queryset=FinishedProducts.objects.all())  # Finished Product ID
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)  # Optional, to be set dynamically

    class Meta:
        model = SalesOrderLine
        fields = [
            'id', 'sales_order', 'product', 'quantity', 
            'unit_price', 'line_total', 'created_at'
        ]

    def validate(self, attrs):
        # Fetch the product price dynamically from FinishedProducts model
        product = attrs.get('product')
        if product:
            attrs['unit_price'] = product.selling_price  # Get product price
            attrs['line_total'] = attrs['unit_price'] * attrs['quantity']  # Calculate line total
        return attrs


class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Suppliers.objects.all())  # Supplier ID

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'order_number', 'supplier', 'order_date', 'due_date', 
            'status', 'total_amount', 'remarks', 'is_deleted', 'created_at'
        ]


class PurchaseOrderLineSerializer(serializers.ModelSerializer):
    purchase_order = serializers.PrimaryKeyRelatedField(queryset=PurchaseOrder.objects.all())  # Purchase Order ID
    material = serializers.PrimaryKeyRelatedField(queryset=RawMaterials.objects.all())  # Raw Material ID
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)  # Optional, to be set dynamically

    class Meta:
        model = PurchaseOrderLine
        fields = [
            'id', 'purchase_order', 'material', 'quantity', 
            'unit_price', 'line_total', 'created_at'
        ]

    def validate(self, attrs):
        # Fetch the material price dynamically from RawMaterials model
        material = attrs.get('material')
        if material:
            attrs['unit_price'] = material.price_per_unit  # Get material price
            attrs['line_total'] = attrs['unit_price'] * attrs['quantity']  # Calculate line total
        return attrs
