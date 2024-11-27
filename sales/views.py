from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope
from .models import Cart, Cart_Line, Favorites, Favorite_Line
from .serializers import CartSerializer, CartLineSerializer, FavoritesSerializer, FavoriteLineSerializer

# Cart Views
class CartListView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def get(self, request):
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

class CartCreateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartDetailView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def get(self, request, pk):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CartUpdateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def put(self, request, pk):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartDeleteView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def delete(self, request, pk):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Cart Line Views
class CartLineListView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def get(self, request):
        cart_lines = Cart_Line.objects.all()
        serializer = CartLineSerializer(cart_lines, many=True)
        return Response(serializer.data)

class CartLineCreateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def post(self, request):
        serializer = CartLineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartLineDetailView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def get(self, request, pk):
        try:
            cart_line = Cart_Line.objects.get(pk=pk)
        except Cart_Line.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartLineSerializer(cart_line)
        return Response(serializer.data)

class CartLineUpdateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def put(self, request, pk):
        try:
            cart_line = Cart_Line.objects.get(pk=pk)
        except Cart_Line.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartLineSerializer(cart_line, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartLineDeleteView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def delete(self, request, pk):
        try:
            cart_line = Cart_Line.objects.get(pk=pk)
        except Cart_Line.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart_line.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Favorites Views
class FavoritesListView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def get(self, request):
        favorites = Favorites.objects.all()
        serializer = FavoritesSerializer(favorites, many=True)
        return Response(serializer.data)

class FavoritesCreateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def post(self, request):
        serializer = FavoritesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoritesDetailView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def get(self, request, pk):
        try:
            favorites = Favorites.objects.get(pk=pk)
        except Favorites.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FavoritesSerializer(favorites)
        return Response(serializer.data)

class FavoritesUpdateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def put(self, request, pk):
        try:
            favorites = Favorites.objects.get(pk=pk)
        except Favorites.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FavoritesSerializer(favorites, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoritesDeleteView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def delete(self, request, pk):
        try:
            favorites = Favorites.objects.get(pk=pk)
        except Favorites.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        favorites.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Favorite Line Views
class FavoriteLineListView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def get(self, request):
        favorite_lines = Favorite_Line.objects.all()
        serializer = FavoriteLineSerializer(favorite_lines, many=True)
        return Response(serializer.data)

class FavoriteLineCreateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def post(self, request):
        serializer = FavoriteLineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoriteLineDetailView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def get(self, request, pk):
        try:
            favorite_line = Favorite_Line.objects.get(pk=pk)
        except Favorite_Line.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FavoriteLineSerializer(favorite_line)
        return Response(serializer.data)

class FavoriteLineUpdateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def put(self, request, pk):
        try:
            favorite_line = Favorite_Line.objects.get(pk=pk)
        except Favorite_Line.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FavoriteLineSerializer(favorite_line, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoriteLineDeleteView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['enduser']

    def delete(self, request, pk):
        try:
            favorite_line = Favorite_Line.objects.get(pk=pk)
        except Favorite_Line.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        favorite_line.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
