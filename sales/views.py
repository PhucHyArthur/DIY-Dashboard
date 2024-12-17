from rest_framework.viewsets import ModelViewSet
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from users.validators import TokenHasAnyScope
from .models import Cart_Line, Favorite_Line
from .serializers import CartLineSerializer, FavoriteLineSerializer


class ScopedModelViewSet(ModelViewSet):
    """
    Base ViewSet với `scope` cố định là `enduser`.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasAnyScope]
    required_scopes = ['enduser']


class CartLineViewSet(ScopedModelViewSet):
    """
    ViewSet cho Cart Lines với Scoped Permissions.
    """
    queryset = Cart_Line.objects.all()
    serializer_class = CartLineSerializer

    def get_queryset(self):
        """
        Lọc các Cart Lines theo user hiện tại.
        """
        user_id = self.request.user.id
        return Cart_Line.objects.filter(user__id=user_id)

    def perform_create(self, serializer):
        """
        Gắn user hiện tại vào Cart_Line khi tạo mới.
        """
        serializer.save(user=self.request.user)


class FavoriteLineViewSet(ScopedModelViewSet):
    """
    ViewSet cho Favorite Lines với Scoped Permissions.
    """
    queryset = Favorite_Line.objects.all()
    serializer_class = FavoriteLineSerializer

    def get_queryset(self):
        """
        Lọc các Favorite Lines theo user hiện tại.
        """
        user_id = self.request.user.id
        return Favorite_Line.objects.filter(user__id=user_id)

    def perform_create(self, serializer):
        """
        Gắn user hiện tại vào Favorite_Line khi tạo mới.
        """
        serializer.save(user=self.request.user)
  