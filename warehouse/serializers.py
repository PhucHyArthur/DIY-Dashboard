from rest_framework import serializers
from .models import Warehouse, Zone, Aisle, Rack, Location

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'address', 'capacity', 'description', 'is_deleted', 'is_fulled']

class ZoneSerializer(serializers.ModelSerializer):
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())
    warehouse_detail = WarehouseSerializer(source='warehouse', read_only=True)
    is_capacity_exceeded = serializers.SerializerMethodField()

    class Meta:
        model = Zone
        fields = ['id', 'warehouse', 'warehouse_detail', 'name', 'capacity', 'number_of_aisles', 'description', 'is_deleted', 'is_fulled', 'is_capacity_exceeded']

    def get_is_capacity_exceeded(self, obj):
        return obj.is_capacity_exceeded()

class AisleSerializer(serializers.ModelSerializer):
    zone = serializers.PrimaryKeyRelatedField(queryset=Zone.objects.all())
    zone_detail = ZoneSerializer(source='zone', read_only=True)

    class Meta:
        model = Aisle
        fields = ['id', 'zone', 'zone_detail', 'name', 'number_of_racks', 'description', 'is_deleted']

class RackSerializer(serializers.ModelSerializer):
    aisle = serializers.PrimaryKeyRelatedField(queryset=Aisle.objects.all())

    class Meta:
        model = Rack
        fields = ['id', 'aisle', 'name', 'capacity', 'description', 'is_deleted', 'is_fulled']

    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Capacity must be greater than 0.")
        return value

class LocationSerializer(serializers.ModelSerializer):
    rack = serializers.PrimaryKeyRelatedField(queryset=Rack.objects.all())

    class Meta:
        model = Location
        fields = ['id', 'rack', 'bin_number', 'description', 'quantity', 'is_deleted', 'is_fulled']
