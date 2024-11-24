from rest_framework import serializers
from .models import Warehouse, Zone, Aisle, Rack, Location

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'address', 'capacity', 'description', 'is_deleted', 'is_fulled']

class ZoneSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer()

    class Meta:
        model = Zone
        fields = ['id', 'warehouse', 'name', 'capacity', 'description', 'is_deleted', 'is_fulled']

class AisleSerializer(serializers.ModelSerializer):
    zone = ZoneSerializer()

    class Meta:
        model = Aisle
        fields = ['id', 'zone', 'name', 'capacity', 'description', 'is_deleted', 'is_fulled']

class RackSerializer(serializers.ModelSerializer):
    aisle = AisleSerializer()

    class Meta:
        model = Rack
        fields = ['id', 'aisle', 'name', 'capacity', 'description', 'is_deleted', 'is_fulled']

class LocationSerializer(serializers.ModelSerializer):
    rack = RackSerializer()

    class Meta:
        model = Location
        fields = ['id', 'rack', 'bin_number', 'description', 'quantity', 'is_deleted', 'is_fulled']
