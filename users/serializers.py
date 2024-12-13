from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role

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
    
    def update(self, instance, validated_data):
        validated_data['scopes'] = ' '.join(validated_data.pop('scopes'))
        return super().update(instance, validated_data)
    

class UserRegisterSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(write_only=True) 

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'role_name', 'email']

    def create(self, validated_data):
        role_name = validated_data.pop('role_name')
        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            raise serializers.ValidationError({"role_name": "Role does not exist."})

        user = get_user_model().objects.create_user(**validated_data)
        user.role = role
        user.is_staff = True
        user.save()
        return user

class EmployeeListSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name', read_only=True)  # Hiển thị tên Role

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'address', 'hire_date', 'is_active', 'is_delete']

class ClientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']  # Chỉ yêu cầu hai trường này

    def create(self, validated_data):
        try:
            role = Role.objects.get(name="EndUser")
        except Role.DoesNotExist:
            raise serializers.ValidationError({"role_name": "Default role 'EndUser' does not exist."})

        user = get_user_model().objects.create_user(**validated_data)
        user.role = role 
        user.is_staff = False
        user.save()
        return user

class ClientDetailSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'address', 'email', 'role']