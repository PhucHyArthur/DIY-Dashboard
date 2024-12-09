from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from users.validators import TokenHasAnyScope
from .models import Warehouse, Zone, Aisle, Rack, Location
from .serializers import WarehouseSerializer, ZoneSerializer, AisleSerializer, RackSerializer, LocationSerializer

class ScopedModelViewSet(ModelViewSet):
    """
    Base ViewSet để ánh xạ required_scopes theo từng hành động.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasAnyScope]

    def get_permissions(self):
        """
        Ánh xạ required_scopes theo từng hành động.
        """
        action_scopes = {
            'list': ['warehouse_read'],
            'retrieve': ['warehouse_read'],
            'create': ['warehouse_create'],
            'update': ['warehouse_update'],
            'partial_update': ['warehouse_update'],
            'destroy': ['warehouse_delete']
        }
        self.required_scopes = action_scopes.get(self.action, [])
        return super().get_permissions()

class LocationViewSet(ScopedModelViewSet):
    """
    ViewSet để quản lý Location (CRUD).
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

# Warehouse ViewSet
class WarehouseViewSet(ScopedModelViewSet):
    """
    ViewSet để quản lý Warehouse (CRUD).
    """
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


# Zone ViewSet
class ZoneViewSet(ScopedModelViewSet):
    """
    ViewSet để quản lý Zone (CRUD).
    """
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    def perform_create(self, serializer):
        """
        Kiểm tra số lượng zones trước khi tạo.
        """
        warehouse = serializer.validated_data.get('warehouse')
        if warehouse.zones.count() >= warehouse.capacity:
            raise serializers.ValidationError("The number of zones has exceeded the warehouse capacity.")
        serializer.save()


# Aisle ViewSet
class AisleViewSet(ScopedModelViewSet):
    """
    ViewSet để quản lý Aisle (CRUD).
    """
    queryset = Aisle.objects.all()
    serializer_class = AisleSerializer

    def perform_create(self, serializer):
        """
        Kiểm tra số lượng aisles trước khi tạo.
        """
        zone = serializer.validated_data.get('zone')
        if zone.aisles.count() >= zone.number_of_aisles:
            raise serializers.ValidationError("The number of aisles has exceeded the zone capacity.")
        serializer.save()


# Rack ViewSet
class RackViewSet(ScopedModelViewSet):
    """
    ViewSet để quản lý Rack (CRUD).
    """
    queryset = Rack.objects.all()
    serializer_class = RackSerializer

    def perform_create(self, serializer):
        """
        Kiểm tra capacity trước khi tạo.
        """
        aisle = serializer.validated_data.get('aisle')
        if aisle.racks.count() >= aisle.number_of_racks:
            raise serializers.ValidationError("The number of racks has exceeded the aisle capacity.")
        serializer.save()
