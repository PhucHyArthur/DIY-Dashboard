from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope
from rest_framework.response import Response
from rest_framework import status

from .models import RawMaterials, FinishedProducts
from .serializers import RawMaterialsSerializer, FinishedProductsSerializer


# Raw Materials Views
class ListRawMaterialsView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['raw_materials_read']

    def get(self, request, *args, **kwargs):
        raw_materials = RawMaterials.objects.filter(is_deleted=False)
        data = RawMaterialsSerializer(raw_materials, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class RetrieveRawMaterialView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['raw_materials_read']

    def get(self, request, pk, *args, **kwargs):
        raw_material = RawMaterials.objects.filter(pk=pk, is_deleted=False).first()
        if not raw_material:
            return Response({"error": "Raw material not found."}, status=status.HTTP_404_NOT_FOUND)
        data = RawMaterialsSerializer(raw_material).data
        return Response(data, status=status.HTTP_200_OK)


class CreateRawMaterialView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['raw_materials_create']

    def post(self, request, *args, **kwargs):
        serializer = RawMaterialsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateRawMaterialView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['raw_materials_update']

    def put(self, request, pk, *args, **kwargs):
        raw_material = RawMaterials.objects.filter(pk=pk).first()
        if not raw_material:
            return Response({"error": "Raw material not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = RawMaterialsSerializer(raw_material, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Raw material {raw_material.name} updated successfully."},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteRawMaterialView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['raw_materials_delete']

    def delete(self, request, pk, *args, **kwargs):
        raw_material = RawMaterials.objects.filter(pk=pk).first()
        if not raw_material:
            return Response({"error": "Raw material not found."}, status=status.HTTP_404_NOT_FOUND)

        raw_material.is_deleted = True
        raw_material.save()
        return Response({"message": "Raw material deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Finished Products Views
class ListFinishedProductsView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['finished_products_read']

    def get(self, request, *args, **kwargs):
        finished_products = FinishedProducts.objects.filter(is_deleted=False)
        data = FinishedProductsSerializer(finished_products, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class RetrieveFinishedProductView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['finished_products_read']

    def get(self, request, pk, *args, **kwargs):
        finished_product = FinishedProducts.objects.filter(pk=pk, is_deleted=False).first()
        if not finished_product:
            return Response({"error": "Finished product not found."}, status=status.HTTP_404_NOT_FOUND)
        data = FinishedProductsSerializer(finished_product).data
        return Response(data, status=status.HTTP_200_OK)


class CreateFinishedProductView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['finished_products_create']

    def post(self, request, *args, **kwargs):
        serializer = FinishedProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateFinishedProductView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['finished_products_update']

    def put(self, request, pk, *args, **kwargs):
        finished_product = FinishedProducts.objects.filter(pk=pk).first()
        if not finished_product:
            return Response({"error": "Finished product not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FinishedProductsSerializer(finished_product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Finished product {finished_product.name} updated successfully."},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteFinishedProductView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['finished_products_delete']

    def delete(self, request, pk, *args, **kwargs):
        finished_product = FinishedProducts.objects.filter(pk=pk).first()
        if not finished_product:
            return Response({"error": "Finished product not found."}, status=status.HTTP_404_NOT_FOUND)

        finished_product.is_deleted = True
        finished_product.save()
        return Response({"message": "Finished product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
