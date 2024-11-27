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
    order_lines = SalesOrderLineSerializer(many=True, required=False)  # Đặt trường này không bắt buộc

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'order_number', 'client', 'order_date', 'due_date',
            'status', 'total_amount', 'remarks', 'is_deleted', 'order_lines'
        ]

    def create(self, validated_data):
        # Lấy dữ liệu order_lines (nếu có)
        order_lines_data = validated_data.pop('order_lines', [])
        # Tạo SalesOrder
        sales_order = SalesOrder.objects.create(**validated_data)
        sales_order.save()

        # Xử lý order_lines nếu có dữ liệu
        for order_line_data in order_lines_data:
            product = order_line_data.get('product')
            quantity = order_line_data.get('quantity')

            try:
                product = FinishedProducts.objects.get(id=product.id)
                unit_price = product.selling_price
            except FinishedProducts.DoesNotExist:
                raise serializers.ValidationError(f"Product với ID {product} không tồn tại.")
            line_total = unit_price * quantity
            SalesOrderLine.objects.create(
                sales_order_id=sales_order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total,
            )

        return sales_order

    def update(self, instance, validated_data):
        # Lấy dữ liệu order_lines (nếu có)
        order_lines_data = validated_data.pop('order_lines', None)

        # Cập nhật các trường trong SalesOrder
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        # Nếu có order_lines, cập nhật hoặc tạo mới
        if order_lines_data is not None:
            # Xóa các dòng cũ
            SalesOrderLine.objects.filter(sales_order_id=instance.id).delete()

            # Tạo lại các dòng mới
            for order_line_data in order_lines_data:
                product = order_line_data.get('product')
                quantity = order_line_data.get('quantity')

                try:
                    product = FinishedProducts.objects.get(id=product.id)
                    unit_price = product.selling_price
                except FinishedProducts.DoesNotExist:
                    raise serializers.ValidationError(f"Product với ID {product} không tồn tại.")
                line_total = unit_price * quantity
                SalesOrderLine.objects.create(
                    sales_order_id=instance.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    line_total=line_total,
                )
        return instance

# class PurchaseOrderLineSerializer(serializers.ModelSerializer):
#     material_id = serializers.PrimaryKeyRelatedField(queryset=RawMaterials.objects.all())
#     purchase_order_id = serializers.PrimaryKeyRelatedField(queryset=PurchaseOrder.objects.all(), write_only=True)  # Đảm bảo dùng đúng tên trường

#     class Meta:
#         model = PurchaseOrderLine
#         fields = ['id', 'purchase_order_id', 'material_id', 'quantity', 'unit_price', 'line_total', 'created_at']

#     def create(self, validated_data):
#         # Lấy material_id từ validated_data
#         material = validated_data.get('material_id')  # material_id là đối tượng RawMaterials

#         # Lấy unit_price từ đối tượng material (RawMaterials)
#         unit_price = material.price_per_unit  # Sử dụng price_per_unit thay vì material_id.unit_price

#         # Tính toán line_total
#         validated_data['unit_price'] = unit_price
#         validated_data['line_total'] = validated_data['quantity'] * unit_price
        
#         # Tạo và lưu PurchaseOrderLine
#         purchase_order_line = PurchaseOrderLine(**validated_data)
#         purchase_order_line.save()

#         # Cập nhật total_amount của PurchaseOrder sau khi thêm dòng mới
#         purchase_order_line.purchase_order.update_total_amount()

#         return purchase_order_line
    
class PurchaseOrderLineSerializer(serializers.ModelSerializer) : 
    material = serializers.PrimaryKeyRelatedField(queryset=RawMaterials.objects.all())

    class Meta:
        model = PurchaseOrderLine
        fields = ['material', 'quantity']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Suppliers.objects.all())  # Đổi tên trường thành supplier_id
    order_lines = PurchaseOrderLineSerializer(many=True, required=False)  # Đặt trường này không bắt buộc

    class Meta:
        model = PurchaseOrder
        # fields = ['id', 'order_number', 'supplier', 'order_date', 'due_date', 'status', 'remarks', 'is_deleted']
        fields = ['id', 'order_number', 'supplier', 'order_date', 'due_date', 'status', 'remarks', 'is_deleted', 'order_lines']
    def create(self, validated_data):
        # Lấy dữ liệu order_lines (nếu có)
        order_lines_data = validated_data.pop('order_lines', [])
        # Tạo PurchaseOrder
        purchase_order = PurchaseOrder.objects.create(**validated_data)
        purchase_order.save()
        print(purchase_order)
        # Nếu có dữ liệu order_lines, tạo các PurchaseOrderLine tương ứng
        for order_line_data in order_lines_data:
            material = order_line_data.get('material')
            quantity = order_line_data.get('quantity')

            try:
                material = RawMaterials.objects.get(id=material.id)
                unit_price = material.price_per_unit
            except RawMaterials.DoesNotExist:
                raise serializers.ValidationError(f"Material với ID {material} không tồn tại.")
            line_total = unit_price * quantity
            PurchaseOrderLine.objects.create(
                purchase_order_id=purchase_order.id,
                material_id=material.id,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total,
            ) 

        return purchase_order


