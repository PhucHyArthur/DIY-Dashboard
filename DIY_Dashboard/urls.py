from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from oauth2_provider import urls as oauth2_urls 

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="Mô tả API cho hệ thống",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('payment/', include('payment.urls')),
    path("api/inventory/", include("inventory.urls")),
    path("api/suppliers/", include("suppliers.urls")),
    path("api/warehouses/", include("warehouse.urls")),
    path("api/sales/", include("sales.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/auth/", include("users.urls")),
    path("api/", include(oauth2_urls)),

    # Swagger URLs
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]


