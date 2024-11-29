from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WarehouseViewSet, ZoneViewSet, AisleViewSet, RackViewSet

# Warehouse URLs
warehouse_urls = [
    path('list/', WarehouseViewSet.as_view({'get': 'list'}), name='warehouse-list'),
    path('create/', WarehouseViewSet.as_view({'post': 'create'}), name='warehouse-create'),
    path('detail/<int:pk>/', WarehouseViewSet.as_view({'get': 'retrieve'}), name='warehouse-detail'),
    path('edit/<int:pk>/', WarehouseViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='warehouse-edit'),
    path('delete/<int:pk>/', WarehouseViewSet.as_view({'delete': 'destroy'}), name='warehouse-delete'),
]

# Zone URLs
zone_urls = [
    path('list/', ZoneViewSet.as_view({'get': 'list'}), name='zone-list'),
    path('create/', ZoneViewSet.as_view({'post': 'create'}), name='zone-create'),
    path('detail/<int:pk>/', ZoneViewSet.as_view({'get': 'retrieve'}), name='zone-detail'),
    path('edit/<int:pk>/', ZoneViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='zone-edit'),
    path('delete/<int:pk>/', ZoneViewSet.as_view({'delete': 'destroy'}), name='zone-delete'),
]

# Aisle URLs
aisle_urls = [
    path('list/', AisleViewSet.as_view({'get': 'list'}), name='aisle-list'),
    path('create/', AisleViewSet.as_view({'post': 'create'}), name='aisle-create'),
    path('detail/<int:pk>/', AisleViewSet.as_view({'get': 'retrieve'}), name='aisle-detail'),
    path('edit/<int:pk>/', AisleViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='aisle-edit'),
    path('delete/<int:pk>/', AisleViewSet.as_view({'delete': 'destroy'}), name='aisle-delete'),
]

# Rack URLs
rack_urls = [
    path('list/', RackViewSet.as_view({'get': 'list'}), name='rack-list'),
    path('create/', RackViewSet.as_view({'post': 'create'}), name='rack-create'),
    path('detail/<int:pk>/', RackViewSet.as_view({'get': 'retrieve'}), name='rack-detail'),
    path('edit/<int:pk>/', RackViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='rack-edit'),
    path('delete/<int:pk>/', RackViewSet.as_view({'delete': 'destroy'}), name='rack-delete'),
]

# Main urlpatterns
urlpatterns = [
    # Warehouse URLs
    path('', include((warehouse_urls, 'warehouses'))),

    # Zone URLs
    path('zones/', include((zone_urls, 'zones'))),

    # Aisle URLs
    path('aisles/', include((aisle_urls, 'aisles'))),

    # Rack URLs
    path('racks/', include((rack_urls, 'racks'))),
]
