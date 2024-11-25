from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from oauth2_provider.models import AccessToken as OAuth2AccessToken
from django.contrib.auth import get_user_model

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    scopes = models.TextField()

    def __str__(self):
        return self.name

    def get_scopes(self):
        return self.scopes.split()

class Employee(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    hire_date = models.DateField(null=True, blank=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role.name if self.role else 'No Role'})"

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

