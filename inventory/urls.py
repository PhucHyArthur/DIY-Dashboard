from django.urls import path
from .views import (
    ListRawMaterialsView, RetrieveRawMaterialView, CreateRawMaterialView, UpdateRawMaterialView, DeleteRawMaterialView,
    ListFinishedProductsView, RetrieveFinishedProductView, CreateFinishedProductView, UpdateFinishedProductView, DeleteFinishedProductView
)

urlpatterns = [
    # Raw Materials URLs
    path('raw-materials/', ListRawMaterialsView.as_view(), name='list_raw_materials'),
    path('raw-materials/<int:pk>/', RetrieveRawMaterialView.as_view(), name='retrieve_raw_material'),
    path('raw-materials/create/', CreateRawMaterialView.as_view(), name='create_raw_material'),
    path('raw-materials/update/<int:pk>/', UpdateRawMaterialView.as_view(), name='update_raw_material'),
    path('raw-materials/delete/<int:pk>/', DeleteRawMaterialView.as_view(), name='delete_raw_material'),

    # Finished Products URLs
    path('finished-products/', ListFinishedProductsView.as_view(), name='list_finished_products'),
    path('finished-products/<int:pk>/', RetrieveFinishedProductView.as_view(), name='retrieve_finished_product'),
    path('finished-products/create/', CreateFinishedProductView.as_view(), name='create_finished_product'),
    path('finished-products/update/<int:pk>/', UpdateFinishedProductView.as_view(), name='update_finished_product'),
    path('finished-products/delete/<int:pk>/', DeleteFinishedProductView.as_view(), name='delete_finished_product'),
]
