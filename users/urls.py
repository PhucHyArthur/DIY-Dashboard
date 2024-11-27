from django.urls import path, include
from .views import RegisterEmployeeView, RegisterRoleView, CustomTokenView, EmployeeListView, UpdateEmployeeView, DeleteEmployeeView, RoleListView, UpdateRoleView, DeleteRoleView

urlpatterns = [
    path('employees/register/', RegisterEmployeeView.as_view(), name='register-employee'),
    path('employees/list/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', UpdateEmployeeView.as_view(), name='update-employee'),
    path('employees/delete/<int:pk>/', DeleteEmployeeView.as_view(), name='delete-employee'),    path('roles/register/', RegisterRoleView.as_view(), name='register-role'),
    path("o/token/", CustomTokenView.as_view(), name="custom-token"),
    path('roles/register/', RegisterRoleView.as_view(), name='register-role'),
    path('roles/', RoleListView.as_view(), name='role-list'),
    path('roles/<int:pk>/', UpdateRoleView.as_view(), name='update-role'),
    path('roles/delete/<int:pk>/', DeleteRoleView.as_view(), name='delete-role'),
]