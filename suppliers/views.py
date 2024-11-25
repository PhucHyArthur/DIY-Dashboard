from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasScope
from .models import Suppliers, Representative
from .serializers import SuppliersSerializer, RepresentativeSerializer

class SuppliersCreateView(APIView):
    """
    API to create a supplier.
    Requires 'suppliers_create' scope.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['suppliers_create']

    def post(self, request, *args, **kwargs):
        serializer = SuppliersSerializer(data=request.data)
        if serializer.is_valid():
            representative_data = request.data.get('representative')
            if representative_data:
                rep_serializer = RepresentativeSerializer(data=representative_data)
                if rep_serializer.is_valid():
                    representative = rep_serializer.save()
                    serializer.save(representative=representative)
                else:
                    return Response(rep_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Representative data is required."}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SuppliersListView(APIView):
    """
    API to list suppliers.
    Requires 'suppliers_read' scope.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['suppliers_read']

    def get(self, request, *args, **kwargs):
        suppliers = Suppliers.objects.all()
        serializer = SuppliersSerializer(suppliers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SuppliersDetailView(APIView):
    """
    API to retrieve, update, or delete a supplier.
    Requires relevant scopes for each action.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = []  # Định nghĩa mặc định để tránh lỗi

    def get(self, request, pk, *args, **kwargs):
        # Định nghĩa required_scopes cho GET
        self.required_scopes = ['suppliers_read']
        self.check_permissions(request)
        try:
            supplier = Suppliers.objects.get(pk=pk)
            serializer = SuppliersSerializer(supplier)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Suppliers.DoesNotExist:
            return Response({"error": "Supplier not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, *args, **kwargs):
        # Định nghĩa required_scopes cho PUT
        self.required_scopes = ['suppliers_update']
        self.check_permissions(request)
        try:
            supplier = Suppliers.objects.get(pk=pk)
            serializer = SuppliersSerializer(supplier, data=request.data)
            if serializer.is_valid():
                representative_data = request.data.get('representative')
                if representative_data:
                    rep_serializer = RepresentativeSerializer(supplier.representative, data=representative_data)
                    if rep_serializer.is_valid():
                        rep_serializer.save()
                    else:
                        return Response(rep_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Suppliers.DoesNotExist:
            return Response({"error": "Supplier not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, *args, **kwargs):
        # Định nghĩa required_scopes cho DELETE
        self.required_scopes = ['suppliers_delete']
        self.check_permissions(request)
        try:
            supplier = Suppliers.objects.get(pk=pk)
            supplier.delete()
            return Response({"message": "Supplier deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Suppliers.DoesNotExist:
            return Response({"error": "Supplier not found."}, status=status.HTTP_404_NOT_FOUND)
