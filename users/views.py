import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDict
from django.utils.timezone import now
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from oauth2_provider.views import TokenView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from rest_framework import status
from rest_framework.response import Response

from users.models import Employee, Role
from .serializers import ClientDetailSerializer, ClientRegisterSerializer, EmployeeListSerializer, RoleSerializer, UserRegisterSerializer
from .validators import TokenHasAnyScope
from .tokens import account_activation_token

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

def send_activation_email(user, activation_link):
    subject = "Activate Your Account"
    from_email = "diystore2024@gmail.com"
    to_email = [user.email]

    text_content = f"Hi {user.username},\n\nClick the link below to activate your account:\n{activation_link}"
    html_content = f"""
    <p>Hi {user.username},</p>
    <p>Click the link below to activate your account:</p>
    <a href="{activation_link}">Activate Your Account</a>
    """

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()    
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
        user = serializer.save(is_active=False)  # Tài khoản chưa kích hoạt
        
        # Tạo link kích hoạt tài khoản
        activation_link = f"https://diy-frontend.onrender.com/activate-account?uid={user.id}&token={account_activation_token.make_token(user)}"
        
        # Gửi email kích hoạt
        send_activation_email(user, activation_link)

        
        return Response(
            {"message": f"User {user.username} created successfully. Activation email sent."},
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
                    "message": f"Client {client.username} registered successfully.",
                    "id": client.id,  # Trả về thêm ID của client
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClientViewSet(ModelViewSet):
    """
    ViewSet cho các hành động liên quan đến client (enduser).
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasAnyScope]
    queryset = Employee.objects.all()
    serializer_class = ClientDetailSerializer

    def get_permissions(self):
        """
        Đặt required_scopes theo từng hành động.
        """
        action_scopes = {
            'list': ['users_read'],  # Nhân viên có thể xem danh sách (nếu cần)
            'retrieve': ['enduser'],  # Chỉ enduser (client) mới xem được thông tin của chính họ
            'update': ['enduser'],   # Chỉ enduser có thể cập nhật thông tin cá nhân
            'partial_update': ['enduser'],
            'destroy': ['enduser']   # Chỉ enduser mới có thể xóa tài khoản của họ
        }
        self.required_scopes = action_scopes.get(self.action, [])
        return super().get_permissions()

    def get_queryset(self):
        # Khởi tạo `required_scopes` mặc định nếu chưa có
        self.required_scopes = getattr(self, 'required_scopes', [])
        
        # Logic lọc queryset
        if 'enduser' in self.required_scopes:
            return self.queryset.filter(id=self.request.user.id)
        return self.queryset

    def perform_update(self, serializer):
        instance = self.get_object()
        if self.request.user.id != instance.id:  # Sửa instance.user.id thành instance.id
            raise PermissionDenied("You do not have permission to update this client.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.id != instance.id:  # Sửa instance.user.id thành instance.id
            raise PermissionDenied("You do not have permission to delete this client.")
        instance.delete()


class ChangePasswordView(APIView):
    """
    API để người dùng đổi mật khẩu.
    """
    authentication_classes = [OAuth2Authentication]

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        # Xác minh dữ liệu đầu vào
        if not all(k in data for k in ("current_password", "new_password", "confirm_password")):
            return Response(
                {"error": "Missing required fields (current_password, new_password, confirm_password)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_password = data.get("current_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        # Kiểm tra mật khẩu hiện tại
        if not check_password(current_password, user.password):
            return Response(
                {"error": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Kiểm tra mật khẩu mới và xác nhận
        if new_password != confirm_password:
            return Response(
                {"error": "New password and confirm password do not match."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Đổi mật khẩu
        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )
    
class ActivateAccountView(APIView):
    def get(self, request, uid, token, *args, **kwargs):
        try:
            user = get_object_or_404(User, pk=uid)
            
            if user.is_active:
                return Response(
                    {"message": "Account is already activated."},
                    status=status.HTTP_200_OK
                )
            
            # Kiểm tra token
            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return Response(
                    {"message": "Account activated successfully!"},
                    status=status.HTTP_200_OK
                )
            else:
                raise ValidationError("Token is invalid or has expired.")
        
        except ValidationError as e:
            return Response(
                {"message": "Activation failed.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            # Xử lý các lỗi khác
            return Response(
                {"message": "An unexpected error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )