from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from users.validators import TokenHasAnyScope
from .models import SalesOrder, SalesOrderLine, PurchaseOrder, PurchaseOrderLine
from .serializers import (
    SalesOrderSerializer,
    SalesOrderLineSerializer,
    PurchaseOrderSerializer,
    PurchaseOrderLineSerializer,
)

class ScopedModelViewSet(ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasAnyScope]

    def get_permissions(self):
        """
        Gán `required_scopes` theo hành động và cho phép ViewSet cụ thể bổ sung scope.
        """
        # Các scope mặc định theo hành động
        action_scopes = {
            'list': [f'{self.scope_prefix}_read'],
            'retrieve': [f'{self.scope_prefix}_read'],
            'create': [f'{self.scope_prefix}_create'],
            'update': [f'{self.scope_prefix}_update'],
            'partial_update': [f'{self.scope_prefix}_update'],
            'destroy': [f'{self.scope_prefix}_delete'],
        }

        # Lấy danh sách scope cho hành động hiện tại
        self.required_scopes = action_scopes.get(self.action, [])

        # Nếu có `extra_scopes` (ghi đè trong ViewSet con), thêm vào
        extra_scopes = getattr(self, 'extra_scopes', [])
        self.required_scopes.extend(extra_scopes)

        return super().get_permissions()

# Sales Order ViewSet
class SalesOrderViewSet(ScopedModelViewSet):
    """
    ViewSet để quản lý SalesOrder (CRUD).
    """
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    scope_prefix = 'sales_orders'
    extra_scopes = ['enduser']

    def create(self, request, *args, **kwargs):
        """
        Tạo SalesOrder với các SalesOrderLine liên quan.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sales_order = serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Cập nhật SalesOrder và các dòng SalesOrderLine liên quan.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Xử lý các dòng order_lines nếu có
        order_lines_data = request.data.get('order_lines', None)
        if order_lines_data is not None:
            # Xóa các dòng cũ
            SalesOrderLine.objects.filter(sales_order=instance).delete()
            # Tạo các dòng mới
            for order_line_data in order_lines_data:
                order_line_serializer = SalesOrderLineSerializer(data=order_line_data)
                order_line_serializer.is_valid(raise_exception=True)
                order_line_serializer.save(sales_order=instance)

        return Response(serializer.data)


# Sales Order Line ViewSet
class SalesOrderLineViewSet(ScopedModelViewSet):
    """
    ViewSet để quản lý SalesOrderLine (CRUD).
    """
    queryset = SalesOrderLine.objects.all()
    serializer_class = SalesOrderLineSerializer
    scope_prefix = 'sales_orders'
    extra_scopes = ['enduser']


# Purchase Order ViewSet
class PurchaseOrderViewSet(ScopedModelViewSet):
    """
    ViewSet để quản lý PurchaseOrder (CRUD).
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    scope_prefix = 'purchases_orders'

    def create(self, request, *args, **kwargs):
        """
        Tạo PurchaseOrder với các PurchaseOrderLine liên quan.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        purchase_order = serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Cập nhật PurchaseOrder và các dòng PurchaseOrderLine liên quan.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# Purchase Order Line ViewSet
class PurchaseOrderLineViewSet(ScopedModelViewSet):
    """
    ViewSet để quản lý PurchaseOrderLine (CRUD).
    """
    queryset = PurchaseOrderLine.objects.all()
    serializer_class = PurchaseOrderLineSerializer
    scope_prefix = 'purchases_orders'
