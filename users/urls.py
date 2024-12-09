from django.urls import path, include
from .views import ChangePasswordView, ClientRegisterView, ClientViewSet, CustomTokenView, RoleViewSet, EmployeeViewSet

# Role URLs
role_urls = [
    path('list/', RoleViewSet.as_view({'get': 'list'}), name='role-list'),
    path('create/', RoleViewSet.as_view({'post': 'create'}), name='role-create'),
    path('detail/<int:pk>/', RoleViewSet.as_view({'get': 'retrieve'}), name='role-detail'),
    path('edit/<int:pk>/', RoleViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='role-edit'),
    path('delete/<int:pk>/', RoleViewSet.as_view({'delete': 'destroy'}), name='role-delete'),
]

# Employee URLs
employee_urls = [
    path('list/', EmployeeViewSet.as_view({'get': 'list'}), name='employee-list'),
    path('create/', EmployeeViewSet.as_view({'post': 'create'}), name='employee-create'),
    path('detail/<int:pk>/', EmployeeViewSet.as_view({'get': 'retrieve'}), name='employee-detail'),
    path('edit/<int:pk>/', EmployeeViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='employee-edit'),
    path('delete/<int:pk>/', EmployeeViewSet.as_view({'delete': 'destroy'}), name='employee-delete'),
]

# Client URLs
client_urls = [
    path('list/', ClientViewSet.as_view({'get': 'list'}), name='client-list'),
    path('create/', ClientViewSet.as_view({'post': 'create'}), name='client-create'),
    path('detail/<int:pk>/', ClientViewSet.as_view({'get': 'retrieve'}), name='client-detail'),
    path('edit/<int:pk>/', ClientViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='client-edit'),
    path('delete/<int:pk>/', ClientViewSet.as_view({'delete': 'destroy'}), name='client-delete'),
]

# Main urlpatterns
urlpatterns = [
    # Login URL
    path("o/token/", CustomTokenView.as_view(), name="custom-token"),
    
    # Role URLs
    path('roles/', include((role_urls, 'roles'))),

    # Employee URLs
    path('employees/', include((employee_urls, 'employees'))),

    # Client URLs
    path('clients/', include((client_urls, 'clients'))),

    # Client Registration (separate API)
    path('clients/register/', ClientRegisterView.as_view(), name='client-register'),

    # Change Password URL
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
