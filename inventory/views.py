from rest_framework.viewsets import ModelViewSet
from .models import RawMaterials, FinishedProducts, Location
from .serializers import RawMaterialsSerializer, FinishedProductsSerializer, LocationSerializer
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope


class ScopedModelViewSet(ModelViewSet):
    """
    Base ViewSet để ánh xạ `required_scopes` cho từng hành động.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    scope_prefix = ''  # Prefix động sẽ được gán trong các lớp con

    def get_permissions(self):
        """
        Gán `required_scopes` dựa trên hành động hiện tại.
        """
        action_scopes = {
            'list': [f'{self.scope_prefix}_read'],
            'retrieve': [f'{self.scope_prefix}_read'],
            'create': [f'{self.scope_prefix}_create'],
            'update': [f'{self.scope_prefix}_update'],
            'partial_update': [f'{self.scope_prefix}_update'],
            'destroy': [f'{self.scope_prefix}_delete'],
        }
        self.required_scopes = action_scopes.get(self.action, [])
        return super().get_permissions()


class RawMaterialsViewSet(ScopedModelViewSet):
    """
    ViewSet for managing Raw Materials.
    """
    queryset = RawMaterials.objects.all()
    serializer_class = RawMaterialsSerializer
    scope_prefix = 'raw_materials'  # Scope prefix cho Raw Materials

    def get_queryset(self):
        """
        Tùy chỉnh queryset để chỉ trả về các nguyên vật liệu chưa bị xóa.
        """
        return super().get_queryset().filter(is_deleted=False)


class FinishedProductsViewSet(ScopedModelViewSet):
    """
    ViewSet for managing Finished Products.
    """
    queryset = FinishedProducts.objects.all()
    serializer_class = FinishedProductsSerializer
    scope_prefix = 'finished_products'  # Scope prefix cho Finished Products

    def get_queryset(self):
        """
        Tùy chỉnh queryset để chỉ trả về các sản phẩm hoàn thiện chưa bị xóa.
        """
        return super().get_queryset().filter(is_deleted=False)
