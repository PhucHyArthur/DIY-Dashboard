from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from oauth2_provider.models import AccessToken as OAuth2AccessToken
from django.utils.timezone import now
from oauth2_provider.views import TokenView
from django.utils import timezone
from datetime import timedelta

from .serializers import EmployeeCreateSerializer, RoleSerializer
from .models import Role, CustomAccessToken
import json

class LoginView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            raise AuthenticationFailed('Username and password are required')

        User = get_user_model()
        # Xác thực người dùng
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials')

        # Lấy access token và refresh token cho người dùng
        tokens = self.get_tokens_for_user(user)

        return JsonResponse({
            'message': 'Login successful',
            'data': tokens
        }, status=200)
        
    def get_tokens_for_user(self, user):
        # Gọi CustomAccessToken để tạo access token tùy chỉnh
        role = user.role
        scopes = role.scopes if role.scopes else [] 
        refresh = RefreshToken.for_user(user)

        # Dùng CustomAccessToken để tạo token
        access_token = CustomAccessToken.objects.create(
            user=user,
            scope=' '.join(scopes),  # Gán scope vào access token
            expires=timezone.now() + timedelta(seconds=3600),  # Thời gian hết hạn (ví dụ 1 giờ)
        )
        return {
            'refresh_token': str(refresh),
            'access_token': str(access_token),
            'scopes': scopes,
            "role": role.name
        }
class RegisterView(APIView):
    def post(self, request) : 
        serializer = EmployeeCreateSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'User created successfully'}, status=201)
        return JsonResponse(serializer.errors, status=400)
    
class RoleView(APIView):
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return JsonResponse(serializer.data, safe=False)
    
