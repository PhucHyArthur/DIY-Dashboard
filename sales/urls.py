from django.urls import path
from .views import (
    CartLineListView, CartLineCreateView, CartLineUpdateView, CartLineDeleteView,
    FavoriteLineListView, FavoriteLineCreateView,  FavoriteLineUpdateView, FavoriteLineDeleteView,
)

urlpatterns = [
    # Cart Line
    path('cart-lines/<int:user_id>/', CartLineListView.as_view(), name='cart-line-list'),
    path('cart-lines/add/', CartLineCreateView.as_view(), name='cart-line-add'),
    path('cart-lines/update/<int:pk>/', CartLineUpdateView.as_view(), name='cart-line-update'),
    path('cart-lines/delete/<int:pk>/', CartLineDeleteView.as_view(), name='cart-line-delete'),

    # Favorite Line
    path('favorite-lines/<int:user_id>/', FavoriteLineListView.as_view(), name='favorite-line-list'),
    path('favorite-lines/add/', FavoriteLineCreateView.as_view(), name='favorite-line-add'),
    path('favorite-lines/update/<int:pk>/', FavoriteLineUpdateView.as_view(), name='favorite-line-update'),
    path('favorite-lines/delete/<int:pk>/', FavoriteLineDeleteView.as_view(), name='favorite-line-delete'),
]
