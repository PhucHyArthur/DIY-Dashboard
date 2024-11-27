import json
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDict
from django.utils.timezone import now

from oauth2_provider.models import AccessToken, RefreshToken
from oauth2_provider.views import TokenView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Role
from .serializers import RoleSerializer, UserRegisterSerializer

User = get_user_model()

def welcome_view(request):
    return JsonResponse({"message": "Welcome to ERP"})

# API cho Role
class RegisterRoleView(APIView):
    """
    API để tạo Role.
    Yêu cầu scope: users_create
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['users_create']

    def post(self, request, *args, **kwargs):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleListView(APIView):
    """
    API để lấy danh sách Role.
    Yêu cầu scope: users_read
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['users_read']

    def get(self, request, *args, **kwargs):
        roles = Role.objects.all()
        role_data = [{"id": role.id, "name": role.name, "description": role.description} for role in roles]
        return Response(role_data, status=status.HTTP_200_OK)


class UpdateRoleView(APIView):
    """
    API để cập nhật Role.
    Yêu cầu scope: users_update
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['users_update']

    def put(self, request, pk, *args, **kwargs):
        role = Role.objects.filter(pk=pk).first()
        if not role:
            return Response({"error": "Role not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Role {role.name} updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteRoleView(APIView):
    """
    API để xóa Role.
    Yêu cầu scope: users_delete
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['users_delete']

    def delete(self, request, pk, *args, **kwargs):
        role = Role.objects.filter(pk=pk).first()
        if not role:
            return Response({"error": "Role not found."}, status=status.HTTP_404_NOT_FOUND)
        role.delete()
        return Response({"message": "Role deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# API cho Employee
class RegisterEmployeeView(APIView):
    """
    API để đăng ký nhân viên.
    Yêu cầu scope: users_create
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['users_create']

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": f"User {user.username} created successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeListView(APIView):
    """
    API để lấy danh sách nhân viên.
    Yêu cầu scope: users_read
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['users_read']

    def get(self, request, *args, **kwargs):
        employees = User.objects.all()
        employee_data = [{"id": user.id, "username": user.username} for user in employees]
        return Response(employee_data, status=status.HTTP_200_OK)


class UpdateEmployeeView(APIView):
    """
    API để cập nhật thông tin nhân viên.
    Yêu cầu scope: users_update
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['users_update']

    def put(self, request, pk, *args, **kwargs):
        user = User.objects.filter(pk=pk).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserRegisterSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"User {user.username} updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteEmployeeView(APIView):
    """
    API để xóa nhân viên.
    Yêu cầu scope: users_delete
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['users_delete']

    def delete(self, request, pk, *args, **kwargs):
        user = User.objects.filter(pk=pk).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Custom Token View
class CustomTokenView(TokenView):
    """
    API để xử lý việc tạo token với các kiểm tra bổ sung.
    """
    def post(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return JsonResponse(
                {"error": "invalid_request", "error_description": "Content-Type must be application/json"},
                status=400,
            )

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "invalid_request", "error_description": "Invalid JSON format"},
                status=400,
            )

        data["grant_type"] = "password"
        data["client_id"] = getattr(settings, "DEFAULT_CLIENT_ID", None)
        data["client_secret"] = getattr(settings, "DEFAULT_CLIENT_SECRET", None)

        if not data["client_id"] or not data["client_secret"]:
            return JsonResponse(
                {"error": "server_error", "error_description": "Client ID or Client Secret is missing in settings."},
                status=500,
            )

        if "username" not in data or "password" not in data:
            return JsonResponse(
                {"error": "invalid_request", "error_description": "Missing username or password"},
                status=400,
            )

        request.POST = MultiValueDict({key: [value] for key, value in data.items()})
        return super().post(request, *args, **kwargs)
