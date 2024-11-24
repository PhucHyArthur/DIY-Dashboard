from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from django.http import Http404
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from .models import Warehouse, Zone, Aisle, Rack
from .serializers import WarehouseSerializer, ZoneSerializer, AisleSerializer, RackSerializer


# Custom Pagination
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class WarehouseScopedPermission:
    def __init__(self):
        self.scope_mapping = {
            'POST': 'warehouse_create',
            'GET': 'warehouse_read',
            'PUT': 'warehouse_update',
            'DELETE': 'warehouse_delete',
        }

    def has_permission(self, request, view):
        method = request.method
        required_scope = self.scope_mapping.get(method)

        if required_scope and required_scope not in request.auth.scopes:
            raise PermissionDenied(f"You do not have permission to perform '{method}' on this resource.")
        return True


class BaseWarehouse(ViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [WarehouseScopedPermission]
    model = None
    serializer_class = None

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404(f"Object with ID {pk} does not exist.")

    def list(self, request):
        self.permission_classes[0]().has_permission(request, self)
        queryset = self.model.objects.all()
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        self.permission_classes[0]().has_permission(request, self)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create.",
            "errors": serializer.errors
        }, status=400)

    def retrieve(self, request, pk=None):
        self.permission_classes[0]().has_permission(request, self)
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj)
        return Response({
            "message": "Retrieved successfully.",
            "data": serializer.data
        })

    def update(self, request, pk=None):
        self.permission_classes[0]().has_permission(request, self)
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Updated successfully.",
                "data": serializer.data
            })
        return Response({
            "message": "Failed to update.",
            "errors": serializer.errors
        }, status=400)

    def destroy(self, request, pk=None):
        self.permission_classes[0]().has_permission(request, self)
        obj = self.get_object(pk)
        obj.delete()
        return Response({"message": f"Deleted object with ID {pk}."}, status=204)


class WarehouseView(BaseWarehouse):
    model = Warehouse
    serializer_class = WarehouseSerializer


class ZoneView(BaseWarehouse):
    model = Zone
    serializer_class = ZoneSerializer


class AisleView(BaseWarehouse):
    model = Aisle
    serializer_class = AisleSerializer


class RackView(BaseWarehouse):
    model = Rack
    serializer_class = RackSerializer
