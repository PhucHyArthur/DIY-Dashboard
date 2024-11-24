from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Role, Employee, Customer

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']

class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    role = RoleSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'role', 'first_name', 'last_name', 'email', 'phone_number', 'hire_date', 'is_active', 'is_delete']

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Customer
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'created_at', 'is_active', 'is_delete']
