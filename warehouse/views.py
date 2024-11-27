from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope

from .models import Warehouse, Zone, Aisle, Rack
from .serializers import WarehouseSerializer, ZoneSerializer, AisleSerializer, RackSerializer


# Warehouse APIs
class RegisterWarehouseView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_create']

    def post(self, request, *args, **kwargs):
        serializer = WarehouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarehouseListView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_read']

    def get(self, request, *args, **kwargs):
        warehouses = Warehouse.objects.all()
        data = WarehouseSerializer(warehouses, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class UpdateWarehouseView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_update']

    def put(self, request, pk, *args, **kwargs):
        warehouse = Warehouse.objects.filter(pk=pk).first()
        if not warehouse:
            return Response({"error": "Warehouse not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = WarehouseSerializer(warehouse, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Warehouse {warehouse.name} updated successfully."},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteWarehouseView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_delete']

    def delete(self, request, pk, *args, **kwargs):
        warehouse = Warehouse.objects.filter(pk=pk).first()
        if not warehouse:
            return Response({"error": "Warehouse not found."}, status=status.HTTP_404_NOT_FOUND)
        warehouse.delete()
        return Response({"message": "Warehouse deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Zone APIs
class RegisterZoneView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_create']

    def post(self, request, *args, **kwargs):
        serializer = ZoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ZoneListView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_read']

    def get(self, request, *args, **kwargs):
        zones = Zone.objects.all()
        data = ZoneSerializer(zones, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class UpdateZoneView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_update']

    def put(self, request, pk, *args, **kwargs):
        zone = Zone.objects.filter(pk=pk).first()
        if not zone:
            return Response({"error": "Zone not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ZoneSerializer(zone, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Zone {zone.name} updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteZoneView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_delete']

    def delete(self, request, pk, *args, **kwargs):
        zone = Zone.objects.filter(pk=pk).first()
        if not zone:
            return Response({"error": "Zone not found."}, status=status.HTTP_404_NOT_FOUND)
        zone.delete()
        return Response({"message": "Zone deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Aisle APIs
class RegisterAisleView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_create']

    def post(self, request, *args, **kwargs):
        zone_id = request.data.get("zone")
        zone = Zone.objects.filter(pk=zone_id).first()
        if not zone:
            return Response({"error": "Zone not found."}, status=status.HTTP_404_NOT_FOUND)
        if zone.is_aisles_exceeded():
            return Response({"error": "Aisles exceeded for this zone."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AisleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AisleListView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_read']

    def get(self, request, *args, **kwargs):
        aisles = Aisle.objects.all()
        data = AisleSerializer(aisles, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class UpdateAisleView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_update']

    def put(self, request, pk, *args, **kwargs):
        aisle = Aisle.objects.filter(pk=pk).first()
        if not aisle:
            return Response({"error": "Aisle not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AisleSerializer(aisle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Aisle {aisle.name} updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAisleView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_delete']

    def delete(self, request, pk, *args, **kwargs):
        aisle = Aisle.objects.filter(pk=pk).first()
        if not aisle:
            return Response({"error": "Aisle not found."}, status=status.HTTP_404_NOT_FOUND)
        aisle.delete()
        return Response({"message": "Aisle deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Rack APIs
class RegisterRackView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_create']

    def post(self, request, *args, **kwargs):
        aisle_id = request.data.get("aisle")
        aisle = Aisle.objects.filter(pk=aisle_id).first()
        if not aisle:
            return Response({"error": "Aisle not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if aisle.is_racks_exceeded():
            return Response({"error": "Racks exceeded for this aisle."}, status=status.HTTP_400_BAD_REQUEST)
        
        zone = aisle.zone
        if zone.is_capacity_exceeded():
            return Response({"error": "Rack capacity exceeded for this zone."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RackListView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_read']

    def get(self, request, *args, **kwargs):
        racks = Rack.objects.all()
        data = RackSerializer(racks, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class UpdateRackView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_update']

    def put(self, request, pk, *args, **kwargs):
        rack = Rack.objects.filter(pk=pk).first()
        if not rack:
            return Response({"error": "Rack not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = RackSerializer(rack, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Rack {rack.name} updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteRackView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['warehouse_delete']

    def delete(self, request, pk, *args, **kwargs):
        rack = Rack.objects.filter(pk=pk).first()
        if not rack:
            return Response({"error": "Rack not found."}, status=status.HTTP_404_NOT_FOUND)
        rack.delete()
        return Response({"message": "Rack deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
