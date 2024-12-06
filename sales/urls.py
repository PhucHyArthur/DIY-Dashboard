from django.urls import path, include
from .views import CartLineViewSet, FavoriteLineViewSet

# Cart Line URLs
cart_line_urls = [
    path('list/', CartLineViewSet.as_view({'get': 'list'}), name='cart-line-list'),
    path('create/', CartLineViewSet.as_view({'post': 'create'}), name='cart-line-create'),
    path('detail/<int:pk>/', CartLineViewSet.as_view({'get': 'retrieve'}), name='cart-line-detail'),
    path('edit/<int:pk>/', CartLineViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='cart-line-edit'),
    path('delete/<int:pk>/', CartLineViewSet.as_view({'delete': 'destroy'}), name='cart-line-delete'),
]

# Favorite Line URLs
favorite_line_urls = [
    path('list/', FavoriteLineViewSet.as_view({'get': 'list'}), name='favorite-line-list'),
    path('create/', FavoriteLineViewSet.as_view({'post': 'create'}), name='favorite-line-create'),
    path('detail/<int:pk>/', FavoriteLineViewSet.as_view({'get': 'retrieve'}), name='favorite-line-detail'),
    path('edit/<int:pk>/', FavoriteLineViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='favorite-line-edit'),
    path('delete/<int:pk>/', FavoriteLineViewSet.as_view({'delete': 'destroy'}), name='favorite-line-delete'),
]

# Main urlpatterns
urlpatterns = [
    # Cart Lines
    path('cart-lines/', include((cart_line_urls, 'cart-lines'))),

    # Favorite Lines
    path('favorite-lines/', include((favorite_line_urls, 'favorite-lines'))),
]
