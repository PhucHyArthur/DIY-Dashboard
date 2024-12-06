from django.urls import path, include
from .views import RawMaterialsViewSet, FinishedProductsViewSet

# Raw Materials URLs
raw_materials_urls = [
    path('list/', RawMaterialsViewSet.as_view({'get': 'list'}), name='raw-materials-list'),
    path('create/', RawMaterialsViewSet.as_view({'post': 'create'}), name='raw-materials-create'),
    path('detail/<int:pk>/', RawMaterialsViewSet.as_view({'get': 'retrieve'}), name='raw-materials-detail'),
    path('edit/<int:pk>/', RawMaterialsViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='raw-materials-edit'),
    path('delete/<int:pk>/', RawMaterialsViewSet.as_view({'delete': 'destroy'}), name='raw-materials-delete'),
]

# Finished Products URLs
finished_products_urls = [
    path('list/', FinishedProductsViewSet.as_view({'get': 'list'}), name='finished-products-list'),
    path('create/', FinishedProductsViewSet.as_view({'post': 'create'}), name='finished-products-create'),
    path('detail/<int:pk>/', FinishedProductsViewSet.as_view({'get': 'retrieve'}), name='finished-products-detail'),
    path('edit/<int:pk>/', FinishedProductsViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='finished-products-edit'),
    path('delete/<int:pk>/', FinishedProductsViewSet.as_view({'delete': 'destroy'}), name='finished-products-delete'),
]

# Main urlpatterns
urlpatterns = [
    # Raw Materials URLs
    path('raw-materials/', include((raw_materials_urls, 'raw-materials'))),

    # Finished Products URLs
    path('finished-products/', include((finished_products_urls, 'finished-products'))),
]
