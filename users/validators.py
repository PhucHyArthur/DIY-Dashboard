from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.models import AccessToken
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope

class CustomOAuth2Validator(OAuth2Validator):
    def save_bearer_token(self, token, request, *args, **kwargs):
        if request.user:
            token['username'] = request.user.username
            token['user_id'] = request.user.id

        if request.user and hasattr(request.user, 'role') and request.user.role:
            role_scopes = request.user.role.get_scopes()
            token['scope'] = " ".join(role_scopes)

        super().save_bearer_token(token, request, *args, **kwargs)

class TokenHasAnyScope(TokenHasScope):
    """
    Custom permission: Cho phép nếu token chứa ít nhất một scope trong required_scopes.
    """

    def has_permission(self, request, view):
        required_scopes = getattr(view, 'required_scopes', [])
        if not required_scopes:
            return True  

        token = request.auth
        if not token or not hasattr(token, 'scope'):
            return False  

        token_scopes = token.scope.split() 
        return any(scope in token_scopes for scope in required_scopes)
