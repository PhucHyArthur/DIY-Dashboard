from django.urls import path
from .views import SuppliersCreateView, SuppliersListView, SuppliersDetailView

urlpatterns = [
    path('list/', SuppliersListView.as_view(), name='suppliers-list'),
    path('create/', SuppliersCreateView.as_view(), name='suppliers-create'),
    path('detail/<int:pk>/', SuppliersDetailView.as_view(), name='suppliers-detail'),
]
