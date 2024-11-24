from django.urls import path
from .views import RawMaterialView, FinishedProductView

urlpatterns = [
    # Raw Materials
    path('raw_materials/add/', RawMaterialView.as_view({'post': 'create'}), name='raw-materials-add'),
    path('raw_materials/detail/<int:pk>/', RawMaterialView.as_view({'get': 'retrieve'}), name='raw-materials-detail'),
    path('raw_materials/edit/<int:pk>/', RawMaterialView.as_view({'put': 'update'}), name='raw-materials-edit'),
    path('raw_materials/delete/<int:pk>/', RawMaterialView.as_view({'delete': 'destroy'}), name='raw-materials-delete'),

    # Finished Products
    path('finished_products/add/', FinishedProductView.as_view({'post': 'create'}), name='finished-products-add'),
    path('finished_products/detail/<int:pk>/', FinishedProductView.as_view({'get': 'retrieve'}), name='finished-products-detail'),
    path('finished_products/edit/<int:pk>/', FinishedProductView.as_view({'put': 'update'}), name='finished-products-edit'),
    path('finished_products/delete/<int:pk>/', FinishedProductView.as_view({'delete': 'destroy'}), name='finished-products-delete'),
]
