from django.urls import path
from .views import (
    SalesOrderListView, SalesOrderCreateView, SalesOrderDetailView, SalesOrderUpdateView, SalesOrderDeleteView,
    SalesOrderLineListView, SalesOrderLineCreateView, SalesOrderLineDetailView, SalesOrderLineUpdateView, SalesOrderLineDeleteView,
    PurchaseOrderListView, PurchaseOrderCreateView, PurchaseOrderDetailView, PurchaseOrderUpdateView, PurchaseOrderDeleteView,
    PurchaseOrderLineListView, PurchaseOrderLineCreateView, PurchaseOrderLineDetailView, PurchaseOrderLineUpdateView, PurchaseOrderLineDeleteView,
)

urlpatterns = [
    # Sales Order
    path('sales-orders/', SalesOrderListView.as_view(), name='sales-order-list'),
    path('sales-orders/create/', SalesOrderCreateView.as_view(), name='sales-order-create'),
    path('sales-orders/<int:pk>/', SalesOrderDetailView.as_view(), name='sales-order-detail'),
    path('sales-orders/<int:pk>/update/', SalesOrderUpdateView.as_view(), name='sales-order-update'),
    path('sales-orders/<int:pk>/delete/', SalesOrderDeleteView.as_view(), name='sales-order-delete'),

    # Sales Order Line
    path('sales-order-lines/', SalesOrderLineListView.as_view(), name='sales-order-line-list'),
    path('sales-order-lines/create/', SalesOrderLineCreateView.as_view(), name='sales-order-line-create'),
    path('sales-order-lines/<int:pk>/', SalesOrderLineDetailView.as_view(), name='sales-order-line-detail'),
    path('sales-order-lines/<int:pk>/update/', SalesOrderLineUpdateView.as_view(), name='sales-order-line-update'),
    path('sales-order-lines/<int:pk>/delete/', SalesOrderLineDeleteView.as_view(), name='sales-order-line-delete'),

    # Purchase Order
    path('purchase-orders/', PurchaseOrderListView.as_view(), name='purchase-order-list'),
    path('purchase-orders/create/', PurchaseOrderCreateView.as_view(), name='purchase-order-create'),
    path('purchase-orders/<int:pk>/', PurchaseOrderDetailView.as_view(), name='purchase-order-detail'),
    path('purchase-orders/<int:pk>/update/', PurchaseOrderUpdateView.as_view(), name='purchase-order-update'),
    path('purchase-orders/<int:pk>/delete/', PurchaseOrderDeleteView.as_view(), name='purchase-order-delete'),

    # Purchase Order Line
    path('purchase-order-lines/', PurchaseOrderLineListView.as_view(), name='purchase-order-line-list'),
    path('purchase-order-lines/create/', PurchaseOrderLineCreateView.as_view(), name='purchase-order-line-create'),
    path('purchase-order-lines/<int:pk>/', PurchaseOrderLineDetailView.as_view(), name='purchase-order-line-detail'),
    path('purchase-order-lines/<int:pk>/update/', PurchaseOrderLineUpdateView.as_view(), name='purchase-order-line-update'),
    path('purchase-order-lines/<int:pk>/delete/', PurchaseOrderLineDeleteView.as_view(), name='purchase-order-line-delete'),
]
