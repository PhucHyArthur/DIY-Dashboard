from oauth2_provider.contrib.rest_framework import TokenMatchesOASRequirements
from rest_framework.exceptions import PermissionDenied

class CustomTokenMatchesOASRequirements(TokenMatchesOASRequirements):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            method = request.method
            raise PermissionDenied(detail=f"You do not have permission to perform '{method}' on this resource.")
        return True
