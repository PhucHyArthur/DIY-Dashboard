from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role, Employee, Customer
from oauth2_provider.models import Application

class RoleSerializer(serializers.ModelSerializer):
    scopes = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'scopes']
    
    def create(self, validated_data):
        validated_data['scopes'] = ' '.join(validated_data.pop('scopes'))
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['scopes'] = instance.get_scopes()
        return representation

class UserRegisterSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(write_only=True)  # Role được truyền dưới dạng tên

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'role_name']

    def create(self, validated_data):
        role_name = validated_data.pop('role_name')
        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            raise serializers.ValidationError({"role_name": "Role does not exist."})

        user = get_user_model().objects.create_user(**validated_data)
        user.role = role
        user.save()
        return user
    
class EmployeeSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'role', 'first_name', 'last_name', 'email', 'phone_number', 'hire_date', 'is_active', 'is_delete']

class EmployeeCreateSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'password', 'role', 'first_name', 'last_name', 'email', 'phone_number', 'hire_date', 'is_active', 'is_delete']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        employee = get_user_model().objects.create(**validated_data)
        employee.set_password(password)
        employee.save()
        return employee

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone_number', 'address', 'created_at', 'is_active', 'is_delete']