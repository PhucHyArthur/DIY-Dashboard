from django.urls import path
from .views import (
    CartCreateView,
    CartLineListView, CartLineCreateView, CartLineDetailView, CartLineUpdateView, CartLineDeleteView,
    FavoriteLineListView, FavoriteLineCreateView, FavoriteLineDetailView, FavoriteLineUpdateView, FavoriteLineDeleteView,
)

urlpatterns = [
    # Cart Line
    path('cart-lines/<int:pk>/', CartLineListView.as_view(), name='cart-line-list'),
    path('cart-lines/create/', CartLineCreateView.as_view(), name='cart-line-create'),
    path('cart-lines/update/<int:pk>/', CartLineUpdateView.as_view(), name='cart-line-update'),
    path('cart-lines/delete/<int:pk>/', CartLineDeleteView.as_view(), name='cart-line-delete'),

    # Favorite Line
    path('favorite-lines/', FavoriteLineListView.as_view(), name='favorite-line-list'),
    path('favorite-lines/create/', FavoriteLineCreateView.as_view(), name='favorite-line-create'),
    path('favorite-lines/update/<int:pk>/', FavoriteLineUpdateView.as_view(), name='favorite-line-update'),
    path('favorite-lines/delete/<int:pk>/', FavoriteLineDeleteView.as_view(), name='favorite-line-delete'),
]
