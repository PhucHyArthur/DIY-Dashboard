from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasScope
from .models import Cart_Line ,Favorite_Line
from .serializers import CartLineSerializer ,FavoriteLineSerializer

class CartLineListView(APIView):
    """
    API to list cart lines for a user.
    Requires 'cart_lines_read' scope.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['enduser']

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        cart_lines = Cart_Line.objects.filter(user__id=user_id)
        if not cart_lines:
            return Response({"error": "No cart lines found for this user."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CartLineSerializer(cart_lines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CartLineCreateView(APIView):
    """
    API to create a cart line.
    Requires 'cart_lines_create' scope.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['enduser']

    def post(self, request, *args, **kwargs):
        serializer = CartLineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartLineUpdateView(APIView):
    """
    API to update a cart line.
    Requires 'cart_lines_update' scope.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['enduser']

    def put(self, request, *args, **kwargs):
        cart_line = Cart_Line.objects.get(pk=kwargs['pk'])
        serializer = CartLineSerializer(cart_line, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartLineDeleteView(APIView):
    """
    API to delete a cart line.
    Requires 'cart_lines_delete' scope.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['enduser']

    def delete(self, request, *args, **kwargs):
        cart_line = Cart_Line.objects.get(pk=kwargs['pk'])
        cart_line.delete()
        return Response({"message": "Cart line deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class FavoriteLineListView(APIView):
    """
    API to list favorite lines for a user.
    Requires 'favorite_lines_read' scope.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['enduser']

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        favorite_lines = Favorite_Line.objects.filter(user__id=user_id)
        if not favorite_lines:
            return Response({"error": "No favorite lines found for this user."}, status=status.HTTP_404_NOT_FOUND)
        serializer = FavoriteLineSerializer(favorite_lines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FavoriteLineCreateView(APIView):
    """
    API to create a favorite line.
    Requires 'favorite_lines_create' scope.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['enduser']

    def post(self, request, *args, **kwargs):
        serializer = FavoriteLineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoriteLineUpdateView(APIView):
    """
    API to update a favorite line.
    Requires 'favorite_lines_update' scope.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['enduser']

    def put(self, request, *args, **kwargs):
        favorite_line = Favorite_Line.objects.get(pk=kwargs['pk'])
        serializer = FavoriteLineSerializer(favorite_line, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoriteLineDeleteView(APIView):
    """
    API to delete a favorite line.
    Requires 'favorite_lines_delete' scope.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['enduser']

    def delete(self, request, *args, **kwargs):
        favorite_line = Favorite_Line.objects.get(pk=kwargs['pk'])
        favorite_line.delete()
        return Response({"message": "Favorite line deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
