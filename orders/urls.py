from django.urls import path, include
from .views import (
    SalesOrderViewSet, SalesOrderLineViewSet,
    PurchaseOrderViewSet, PurchaseOrderLineViewSet
)

# Sales Order URLs
sales_order_urls = [
    path('list/', SalesOrderViewSet.as_view({'get': 'list'}), name='sales-order-list'),
    path('create/', SalesOrderViewSet.as_view({'post': 'create'}), name='sales-order-create'),
    path('detail/<int:pk>/', SalesOrderViewSet.as_view({'get': 'retrieve'}), name='sales-order-detail'),
    path('edit/<int:pk>/', SalesOrderViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='sales-order-edit'),
    path('delete/<int:pk>/', SalesOrderViewSet.as_view({'delete': 'destroy'}), name='sales-order-delete'),
]

# Sales Order Line URLs
sales_order_line_urls = [
    path('list/', SalesOrderLineViewSet.as_view({'get': 'list'}), name='sales-order-line-list'),
    path('create/', SalesOrderLineViewSet.as_view({'post': 'create'}), name='sales-order-line-create'),
    path('detail/<int:pk>/', SalesOrderLineViewSet.as_view({'get': 'retrieve'}), name='sales-order-line-detail'),
    path('edit/<int:pk>/', SalesOrderLineViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='sales-order-line-edit'),
    path('delete/<int:pk>/', SalesOrderLineViewSet.as_view({'delete': 'destroy'}), name='sales-order-line-delete'),
]

# Purchase Order URLs
purchase_order_urls = [
    path('list/', PurchaseOrderViewSet.as_view({'get': 'list'}), name='purchase-order-list'),
    path('create/', PurchaseOrderViewSet.as_view({'post': 'create'}), name='purchase-order-create'),
    path('detail/<int:pk>/', PurchaseOrderViewSet.as_view({'get': 'retrieve'}), name='purchase-order-detail'),
    path('edit/<int:pk>/', PurchaseOrderViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='purchase-order-edit'),
    path('delete/<int:pk>/', PurchaseOrderViewSet.as_view({'delete': 'destroy'}), name='purchase-order-delete'),
]

# Purchase Order Line URLs
purchase_order_line_urls = [
    path('list/', PurchaseOrderLineViewSet.as_view({'get': 'list'}), name='purchase-order-line-list'),
    path('create/', PurchaseOrderLineViewSet.as_view({'post': 'create'}), name='purchase-order-line-create'),
    path('detail/<int:pk>/', PurchaseOrderLineViewSet.as_view({'get': 'retrieve'}), name='purchase-order-line-detail'),
    path('edit/<int:pk>/', PurchaseOrderLineViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='purchase-order-line-edit'),
    path('delete/<int:pk>/', PurchaseOrderLineViewSet.as_view({'delete': 'destroy'}), name='purchase-order-line-delete'),
]

# Main urlpatterns
urlpatterns = [
    # Sales Orders
    path('sales-orders/', include((sales_order_urls, 'sales-orders'))),
    path('sales-order-lines/', include((sales_order_line_urls, 'sales-order-lines'))),

    # Purchase Orders
    path('purchase-orders/', include((purchase_order_urls, 'purchase-orders'))),
    path('purchase-order-lines/', include((purchase_order_line_urls, 'purchase-order-lines'))),
]
