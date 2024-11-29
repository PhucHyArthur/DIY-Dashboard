from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role, Client
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
    role_name = serializers.CharField(write_only=True) 

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

class EmployeeListSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name', read_only=True)  # Hiển thị tên Role

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'address', 'hire_date']

class ClientRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Client
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        try:
            role = Role.objects.get(name='EndUser')
        except Role.DoesNotExist:
            raise serializers.ValidationError({"role_name": "Role 'EndUser' does not exist."})

        User = get_user_model()

        user = User.objects.create_user(username=username, password=password)
        user.role = role  
        user.save()

        client = Client.objects.create(user=user)
        return client

class ClientDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 'address', 'created_at']