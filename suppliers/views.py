from rest_framework.viewsets import ModelViewSet
from .models import Suppliers, Representative
from .serializers import SuppliersSerializer, RepresentativeSerializer
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope


class ScopedModelViewSet(ModelViewSet):
    """
    Base ViewSet để ánh xạ `required_scopes` cho từng hành động.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope] 

    def get_permissions(self):
        """
        Gán `required_scopes` dựa trên hành động hiện tại.
        """
        action_scopes = {
            'list': ['suppliers_read'],
            'retrieve': ['suppliers_read'],
            'create': ['suppliers_create'],
            'update': ['suppliers_update'],
            'partial_update': ['suppliers_update'],
            'destroy': ['suppliers_delete'],
        }
        self.required_scopes = action_scopes.get(self.action, [])
        return super().get_permissions()


class RepresentativeViewSet(ScopedModelViewSet):
    """
    ViewSet for managing Representatives.
    """
    queryset = Representative.objects.all()
    serializer_class = RepresentativeSerializer


class SuppliersViewSet(ScopedModelViewSet):
    """
    ViewSet for managing Suppliers.
    """
    queryset = Suppliers.objects.all()
    serializer_class = SuppliersSerializer
