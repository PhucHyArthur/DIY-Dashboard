from rest_framework import serializers
from .models import Warehouse, Zone, Aisle, Rack, Location

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'address', 'capacity', 'description', 'is_deleted', 'is_fulled']

class ZoneSerializer(serializers.ModelSerializer):
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all(), default=1)

    class Meta:
        model = Zone
        fields = ['id', 'warehouse', 'name', 'capacity', 'number_of_aisles', 'description', 'is_deleted', 'is_fulled']

class AisleSerializer(serializers.ModelSerializer):
    zone = serializers.PrimaryKeyRelatedField(queryset=Zone.objects.all(), default=1)  # Zone ID instead of full details

    class Meta:
        model = Aisle
        fields = ['id', 'zone', 'name', 'number_of_racks', 'description', 'is_deleted']

class RackSerializer(serializers.ModelSerializer):
    aisle = serializers.PrimaryKeyRelatedField(queryset=Aisle.objects.all(), default=1)  # Aisle ID

    class Meta:
        model = Rack
        fields = ['id', 'aisle', 'name', 'capacity', 'description', 'is_deleted', 'is_fulled']

class LocationSerializer(serializers.ModelSerializer):
    rack = serializers.PrimaryKeyRelatedField(queryset=Rack.objects.all(), default=1)  # Rack ID

    class Meta:
        model = Location
        fields = ['id', 'rack', 'bin_number', 'description', 'quantity', 'is_deleted', 'is_fulled']
