from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Role, Employee, Customer

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description' , 'scopes']

class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    role = RoleSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'role', 'first_name', 'last_name', 'email', 'phone_number', 'hire_date', 'is_active', 'is_delete']
        
class EmployeeCreateSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role')

    class Meta:
        model = Employee
        fields = ['id', 'username', 'password', 'role_id', 'first_name', 'last_name', 'email', 'phone_number', 'hire_date', 'is_active', 'is_delete']
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role')
        employee = Employee.objects.create(**validated_data)
        employee.set_password(password)
        employee.role = role
        employee.save()
        return employee

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = Customer
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'created_at', 'is_active', 'is_delete']
        
