from django.urls import path
from .views import (
    RegisterWarehouseView, WarehouseListView, UpdateWarehouseView, DeleteWarehouseView,
    RegisterZoneView, ZoneListView, UpdateZoneView, DeleteZoneView,
    RegisterAisleView, AisleListView, UpdateAisleView, DeleteAisleView,
    RegisterRackView, RackListView, UpdateRackView, DeleteRackView
)

urlpatterns = [
    # Warehouse URLs
    path('', WarehouseListView.as_view(), name='warehouse-list'),
    path('add/', RegisterWarehouseView.as_view(), name='warehouse-add'),
    path('edit/<int:pk>/', UpdateWarehouseView.as_view(), name='warehouse-edit'),
    path('delete/<int:pk>/', DeleteWarehouseView.as_view(), name='warehouse-delete'),

    # Zone URLs
    path('zones/', ZoneListView.as_view(), name='zone-list'),
    path('zones/add/', RegisterZoneView.as_view(), name='zone-add'),
    path('zones/edit/<int:pk>/', UpdateZoneView.as_view(), name='zone-edit'),
    path('zones/delete/<int:pk>/', DeleteZoneView.as_view(), name='zone-delete'),

    # Aisle URLs
    path('aisles/', AisleListView.as_view(), name='aisle-list'),
    path('aisles/add/', RegisterAisleView.as_view(), name='aisle-add'),
    path('aisles/edit/<int:pk>/', UpdateAisleView.as_view(), name='aisle-edit'),
    path('aisles/delete/<int:pk>/', DeleteAisleView.as_view(), name='aisle-delete'),

    # Rack URLs
    path('racks/', RackListView.as_view(), name='rack-list'),
    path('racks/add/', RegisterRackView.as_view(), name='rack-add'),
    path('racks/edit/<int:pk>/', UpdateRackView.as_view(), name='rack-edit'),
    path('racks/delete/<int:pk>/', DeleteRackView.as_view(), name='rack-delete'),
]

