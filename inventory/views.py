from rest_framework.viewsets import ModelViewSet
from .models import RawMaterials, RawMaterialsLine, FinishedProducts
from warehouse.models import Location
from .serializers import (
    RawMaterialsSerializer,
    RawMaterialsLineSerializer,
    FinishedProductsSerializer,
)
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from users.validators import TokenHasAnyScope


class ScopedModelViewSet(ModelViewSet):
    """
    Base ViewSet để ánh xạ `required_scopes` cho từng hành động.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasAnyScope]

    def get_permissions(self):
        """
        Gán `required_scopes` dựa trên hành động hiện tại.
        """
        action_scopes = self.get_action_scopes()
        self.required_scopes = action_scopes.get(self.action, [])
        return super().get_permissions()

    def get_action_scopes(self):
        """
        Phương thức để các ViewSet con định nghĩa scope của từng hành động.
        """
        raise NotImplementedError("Subclasses must implement `get_action_scopes`.")


class RawMaterialsViewSet(ScopedModelViewSet):
    """
    ViewSet for managing Raw Materials.
    """
    queryset = RawMaterials.objects.all()
    serializer_class = RawMaterialsSerializer

    def get_action_scopes(self):
        """
        Scope cho phép người dùng thực hiện các hành động liên quan đến raw materials.
        """
        return {
            'list': ['raw_materials_read'],
            'retrieve': ['raw_materials_read'],
            'create': ['raw_materials_create'],
            'update': ['raw_materials_update'],
            'partial_update': ['raw_materials_update'],
            'destroy': ['raw_materials_delete'],
        }

    def get_queryset(self):
        """
        Tùy chỉnh queryset để chỉ trả về các raw materials chưa bị xóa.
        """
        return super().get_queryset().filter(is_deleted=False)


class RawMaterialsLineViewSet(ScopedModelViewSet):
    """
    ViewSet for managing Raw Materials Lines.
    """
    queryset = RawMaterialsLine.objects.all()
    serializer_class = RawMaterialsLineSerializer

    def get_action_scopes(self):
        """
        Scope cho phép người dùng thực hiện các hành động liên quan đến raw materials lines.
        """
        return {
            'list': ['raw_materials_read'],
            'retrieve': ['raw_materials_read'],
            'create': ['raw_materials_create'],
            'update': ['raw_materials_update'],
            'partial_update': ['raw_materials_update'],
            'destroy': ['raw_materials_delete'],
        }

    def get_queryset(self):
        """
        Tùy chỉnh queryset để chỉ trả về các raw materials lines chưa bị xóa.
        """
        return super().get_queryset().filter(is_deleted=False)


class FinishedProductsViewSet(ScopedModelViewSet):
    """
    ViewSet for managing Finished Products.
    """
    queryset = FinishedProducts.objects.all()
    serializer_class = FinishedProductsSerializer

    def get_action_scopes(self):
        """
        Scope cho phép người dùng thực hiện các hành động liên quan đến finished products.
        """
        return {
            'list': ['finished_products_read', 'enduser'], 
            'retrieve': ['finished_products_read', 'enduser'],
            'create': ['finished_products_create'],
            'update': ['finished_products_update'],
            'partial_update': ['finished_products_update'],
            'destroy': ['finished_products_delete'],
        }

    def get_permissions(self):
        """
        Bỏ qua kiểm tra permission cho action 'list'.
        """
        if self.action == 'list':
            return []  # Không kiểm tra permission
        return super().get_permissions()

    def get_queryset(self):
        """
        Tùy chỉnh queryset để chỉ trả về các sản phẩm hoàn thiện chưa bị xóa.
        """
        return super().get_queryset().filter(is_deleted=False)

