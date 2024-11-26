from django.urls import path
from .views import SuppliersCreateView, SuppliersListView, SuppliersDetailView, SuppliersUpdateView, SuppliersDeleteView

urlpatterns = [
    path('', SuppliersListView.as_view(), name='suppliers-list'),
    path('create/', SuppliersCreateView.as_view(), name='suppliers-create'),
    path('detail/<int:pk>/', SuppliersDetailView.as_view(), name='suppliers-detail'),
    path('update/<int:pk>/', SuppliersUpdateView.as_view(), name='suppliers-update'),
    path('delete/<int:pk>/', SuppliersDeleteView.as_view(), name='suppliers-delete'),
]
