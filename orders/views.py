from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope
from .models import SalesOrder, SalesOrderLine, PurchaseOrder, PurchaseOrderLine
from .serializers import (
    SalesOrderSerializer,
    SalesOrderLineSerializer,
    PurchaseOrderSerializer,
    PurchaseOrderLineSerializer,
)

# Sales Order Views
class SalesOrderListView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['sales_orders_read']

    def get(self, request):
        sales_orders = SalesOrder.objects.all()
        serializer = SalesOrderSerializer(sales_orders, many=True)
        return Response(serializer.data)

class SalesOrderCreateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['sales_orders_create']

    def post(self, request):
        serializer = SalesOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SalesOrderDetailView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['sales_orders_read']

    def get(self, request, pk):
        try:
            sales_order = SalesOrder.objects.get(pk=pk)
        except SalesOrder.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SalesOrderSerializer(sales_order)
        return Response(serializer.data)

class SalesOrderUpdateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['sales_orders_update']

    def put(self, request, pk):
        try:
            sales_order = SalesOrder.objects.get(pk=pk)
        except SalesOrder.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SalesOrderSerializer(sales_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SalesOrderDeleteView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['sales_orders_delete']

    def delete(self, request, pk):
        try:
            sales_order = SalesOrder.objects.get(pk=pk)
        except SalesOrder.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        sales_order.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Sales Order Line Views
class SalesOrderLineListView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['sales_orders_read']

    def get(self, request):
        sales_order_lines = SalesOrderLine.objects.all()
        serializer = SalesOrderLineSerializer(sales_order_lines, many=True)
        return Response(serializer.data)

class SalesOrderLineCreateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['sales_orders_create']

    def post(self, request):
        serializer = SalesOrderLineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SalesOrderLineDetailView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['sales_orders_read']

    def get(self, request, pk):
        try:
            sales_order_line = SalesOrderLine.objects.get(pk=pk)
        except SalesOrderLine.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SalesOrderLineSerializer(sales_order_line)
        return Response(serializer.data)

class SalesOrderLineUpdateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['sales_orders_update']

    def put(self, request, pk):
        try:
            sales_order_line = SalesOrderLine.objects.get(pk=pk)
        except SalesOrderLine.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SalesOrderLineSerializer(sales_order_line, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SalesOrderLineDeleteView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['sales_orders_delete']

    def delete(self, request, pk):
        try:
            sales_order_line = SalesOrderLine.objects.get(pk=pk)
        except SalesOrderLine.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        sales_order_line.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# Purchase Order Views
class PurchaseOrderListView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['purchases_orders_read']

    def get(self, request):
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

class PurchaseOrderCreateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['purchases_orders_create']

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    

class PurchaseOrderDetailView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['purchases_orders_read']

    def get(self, request, pk):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

class PurchaseOrderUpdateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['purchases_orders_update']

    def put(self, request, pk):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderDeleteView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['purchases_orders_delete']

    def delete(self, request, pk):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        purchase_order.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Purchase Order Line Views
class PurchaseOrderLineListView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['purchases_orders_read']

    def get(self, request):
        purchase_order_lines = PurchaseOrderLine.objects.all()
        serializer = PurchaseOrderLineSerializer(purchase_order_lines, many=True)
        return Response(serializer.data)

class PurchaseOrderLineCreateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['purchases_orders_create']

    def post(self, request):
        serializer = PurchaseOrderLineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderLineDetailView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['purchases_orders_read']

    def get(self, request, pk):
        try:
            purchase_order_line = PurchaseOrderLine.objects.get(pk=pk)
        except PurchaseOrderLine.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderLineSerializer(purchase_order_line)
        return Response(serializer.data)

class PurchaseOrderLineUpdateView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['purchases_orders_update']

    def put(self, request, pk):
        try:
            purchase_order_line = PurchaseOrderLine.objects.get(pk=pk)
        except PurchaseOrderLine.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderLineSerializer(purchase_order_line, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderLineDeleteView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['purchases_orders_delete']

    def delete(self, request, pk):
        try:
            purchase_order_line = PurchaseOrderLine.objects.get(pk=pk)
        except PurchaseOrderLine.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        purchase_order_line.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

