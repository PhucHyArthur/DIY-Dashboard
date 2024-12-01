import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDict
from django.utils.timezone import now

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from oauth2_provider.views import TokenView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from rest_framework import status
from rest_framework.response import Response

from users.models import Client, Role
from .serializers import ClientDetailSerializer, ClientRegisterSerializer, EmployeeListSerializer, RoleSerializer, UserRegisterSerializer
from .validators import TokenHasAnyScope

User = get_user_model()

def welcome_view(request):
    return JsonResponse({"message": "Welcome to ERP"})


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

## Role ViewSet
class RoleViewSet(ModelViewSet):
    """
    ViewSet để quản lý Role (CRUD).
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasAnyScope]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_permissions(self):
        """
        Ánh xạ required_scopes theo từng hành động.
        """
        action_scopes = {
            'list': ['users_read'],
            'retrieve': ['users_read'],
            'create': ['users_create'],
            'update': ['users_update'],
            'partial_update': ['users_update'],
            'destroy': ['users_delete']
        }
        self.required_scopes = action_scopes.get(self.action, [])
        return super().get_permissions()

    def perform_update(self, serializer):
        """
        Ghi đè phương thức để thay đổi phản hồi khi cập nhật.
        """
        instance = serializer.save()
        return Response(
            {"message": f"Role {instance.name} updated successfully."},
            status=status.HTTP_200_OK
        )

    def perform_destroy(self, instance):
        """
        Ghi đè phương thức để thay đổi phản hồi khi xóa.
        """
        instance.delete()
        return Response(
            {"message": "Role deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
    
## Employee ViewSet
class EmployeeViewSet(ModelViewSet):
    """
    ViewSet để quản lý nhân viên (CRUD).
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasAnyScope]
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Ánh xạ các scope theo hành động.
        """
        action_scopes = {
            'list': ['users_read'],
            'retrieve': ['users_read'],
            'create': ['users_create'],
            'update': ['users_update'],
            'partial_update': ['users_update'],
            'destroy': ['users_delete']
        }
        self.required_scopes = action_scopes.get(self.action, [])
        return super().get_permissions()

    def get_serializer_class(self):
        """
        Sử dụng serializer khác nhau cho các hành động.
        """
        if self.action in ['list', 'retrieve']:
            return EmployeeListSerializer
        return UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        """
        Tạo mới nhân viên với phản hồi tùy chỉnh.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": f"User {user.username} created successfully."},
            status=status.HTTP_201_CREATED
        )
    
## Client ViewSet
class ClientRegisterView(APIView):
    authentication_classes = []  
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = ClientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save()
            return Response(
                {
                    "message": f"Client {client.user.username} registered successfully.",
                    "client_id": client.id,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClientViewSet(ModelViewSet):
    """
    ViewSet cho các hành động cần scope.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasAnyScope]
    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer

    def get_permissions(self):
        """
        Đặt required_scopes theo từng hành động.
        """
        action_scopes = {
            'list': ['users_read'],
            'retrieve': ['users_read'],
            'update': ['users_update', 'enduser'],
            'partial_update': ['users_update','enduser'],
            'destroy': ['users_delete', 'enduser']
        }
        self.required_scopes = action_scopes.get(self.action, [])
        return super().get_permissions()
    
    def perform_update(self, serializer):
        """
        Ghi đè để kiểm tra quyền trước khi cập nhật.
        """
        instance = self.get_object()
        if self.request.user.id != instance.user.id:
            raise PermissionDenied("You do not have permission to update this client.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Ghi đè để kiểm tra quyền trước khi xóa.
        """
        if self.request.user.id != instance.user.id:
            raise PermissionDenied("You do not have permission to delete this client.")
        instance.delete()