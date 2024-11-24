from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    # register for other users
    path('register/', views.RegisterView.as_view(), name='register'),
    path('roles/', views.RoleView.as_view(), name='roles'), 
]
