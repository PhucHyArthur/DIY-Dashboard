from .models import RawMaterials, FinishedProducts
from .serializers import RawMaterialsSerializer, FinishedProductsSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from DIY_Dashboard.permissions import CustomTokenMatchesOASRequirements
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from django.http import Http404
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BaseMaterialView(ViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [CustomTokenMatchesOASRequirements]
    model = None
    serializer_class = None
    required_alternate_scopes = {}

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404(f"Object with ID {pk} does not exist.")

    def list(self, request):
        queryset = self.model.objects.all()

        # Filtering
        name = request.query_params.get('name', None)
        unit = request.query_params.get('unit', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if unit:
            queryset = queryset.filter(unit__icontains=unit)

        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create.",
            "errors": serializer.errors
        }, status=400)

    def retrieve(self, request, pk=None):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj)
        return Response({
            "message": "Retrieved successfully.",
            "data": serializer.data
        })

    def update(self, request, pk=None):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Updated successfully.",
                "data": serializer.data
            })
        return Response({
            "message": "Failed to update.",
            "errors": serializer.errors
        }, status=400)

    def destroy(self, request, pk=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response({"message": f"Deleted object with ID {pk}."}, status=204)


class RawMaterialView(BaseMaterialView):
    model = RawMaterials
    serializer_class = RawMaterialsSerializer
    required_alternate_scopes = {
        'POST': [['raw_materials_create']],
        'GET': [['raw_materials_read']],
        'PUT': [['raw_materials_update']],
        'DELETE': [['raw_materials_delete']],
    }


class FinishedProductView(BaseMaterialView):
    model = FinishedProducts
    serializer_class = FinishedProductsSerializer
    required_alternate_scopes = {
        'POST': [['finished_products_create']],
        'GET': [['finished_products_read']],
        'PUT': [['finished_products_update']],
        'DELETE': [['finished_products_delete']],
    }
