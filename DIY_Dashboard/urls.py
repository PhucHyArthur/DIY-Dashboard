from django.contrib import admin
from django.urls import path, include
from oauth2_provider import urls as oauth2_urls 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/inventory/", include("inventory.urls")),
    path("api/auth/", include("users.urls")),
    path("api/", include(oauth2_urls))
]
