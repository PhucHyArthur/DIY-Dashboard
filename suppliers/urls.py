from django.urls import path, include
from .views import SuppliersViewSet, RepresentativeViewSet

# Representative URLs
representative_urls = [
    path('list/', RepresentativeViewSet.as_view({'get': 'list'}), name='representative-list'),
    path('create/', RepresentativeViewSet.as_view({'post': 'create'}), name='representative-create'),
    path('detail/<int:pk>/', RepresentativeViewSet.as_view({'get': 'retrieve'}), name='representative-detail'),
    path('edit/<int:pk>/', RepresentativeViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='representative-edit'),
    path('delete/<int:pk>/', RepresentativeViewSet.as_view({'delete': 'destroy'}), name='representative-delete'),
]

# Suppliers URLs
suppliers_urls = [
    path('list/', SuppliersViewSet.as_view({'get': 'list'}), name='suppliers-list'),
    path('create/', SuppliersViewSet.as_view({'post': 'create'}), name='suppliers-create'),
    path('detail/<int:pk>/', SuppliersViewSet.as_view({'get': 'retrieve'}), name='suppliers-detail'),
    path('edit/<int:pk>/', SuppliersViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='suppliers-edit'),
    path('delete/<int:pk>/', SuppliersViewSet.as_view({'delete': 'destroy'}), name='suppliers-delete'),
]

# Main urlpatterns
urlpatterns = [
    path('representatives/', include((representative_urls, 'representatives'))),
    path('', include((suppliers_urls, 'suppliers'))),
]
