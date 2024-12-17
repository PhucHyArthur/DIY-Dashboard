from rest_framework import serializers
from .models import SalesOrder, SalesOrderLine, PurchaseOrder, PurchaseOrderLine
from inventory.models import FinishedProducts, RawMaterials
from suppliers.models import Suppliers
from users.models import Employee

class SalesOrderLineSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=FinishedProducts.objects.all())

    class Meta:
        model = SalesOrderLine
        fields = ['product', 'quantity']

class SalesOrderSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    order_lines = SalesOrderLineSerializer(many=True, required=False)

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'order_number', 'client', 'order_date', 'due_date',
            'status', 'total_amount', 'remarks', 'is_deleted', 'order_lines', 'is_paid'
        ]

    def create(self, validated_data):
        order_lines_data = validated_data.pop('order_lines', [])
        sales_order = SalesOrder.objects.create(**validated_data)

        for order_line_data in order_lines_data:
            product = order_line_data['product']
            quantity = order_line_data['quantity']

            # Lấy giá bán của sản phẩm
            unit_price = product.selling_price
            line_total = unit_price * quantity

            SalesOrderLine.objects.create(
                sales_order=sales_order,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total,
            )

        return sales_order

    def update(self, instance, validated_data):
        order_lines_data = validated_data.pop('order_lines', None)

        # Cập nhật thông tin của SalesOrder
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        if order_lines_data is not None:
            # Xóa các dòng order cũ
            instance.order_lines.all().delete()

            # Tạo các dòng order mới
            for order_line_data in order_lines_data:
                product = order_line_data['product']
                quantity = order_line_data['quantity']

                unit_price = product.selling_price
                line_total = unit_price * quantity

                SalesOrderLine.objects.create(
                    sales_order=instance,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    line_total=line_total,
                )

        return instance

class PurchaseOrderLineSerializer(serializers.ModelSerializer):
    material = serializers.PrimaryKeyRelatedField(queryset=RawMaterials.objects.all())

    class Meta:
        model = PurchaseOrderLine
        fields = ['material', 'quantity', 'unit_price']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Suppliers.objects.all())
    order_lines = PurchaseOrderLineSerializer(many=True, required=False)

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'order_number', 'supplier', 'order_date', 'due_date', 'status', 'remarks', 'is_deleted', 'order_lines']

    def create(self, validated_data):
        order_lines_data = validated_data.pop('order_lines', [])
        purchase_order = PurchaseOrder.objects.create(**validated_data)

        for order_line_data in order_lines_data:
            material = order_line_data['material']
            quantity = order_line_data['quantity']
            unit_price = order_line_data['unit_price']

            line_total = unit_price * quantity

            PurchaseOrderLine.objects.create(
                purchase_order=purchase_order,
                material=material,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total,
            )

        return purchase_order

    def update(self, instance, validated_data):
        order_lines_data = validated_data.pop('order_lines', None)

        # Cập nhật thông tin của PurchaseOrder
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        if order_lines_data is not None:
            # Xóa các dòng order cũ
            instance.order_lines.all().delete()

            # Tạo các dòng order mới
            for order_line_data in order_lines_data:
                material = order_line_data['material']
                quantity = order_line_data['quantity']
                unit_price = order_line_data['unit_price']

                line_total = unit_price * quantity

                PurchaseOrderLine.objects.create(
                    purchase_order=instance,
                    material=material,
                    quantity=quantity,
                    unit_price=unit_price,
                    line_total=line_total,
                )

        return instance
