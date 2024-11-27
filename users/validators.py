from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.models import AccessToken

class CustomOAuth2Validator(OAuth2Validator):
    def save_bearer_token(self, token, request, *args, **kwargs):
        if request.user:
            token['username'] = request.user.username
            token['user_id'] = request.user.id

        if request.user and hasattr(request.user, 'role') and request.user.role:
            role_scopes = request.user.role.get_scopes()
            token['scope'] = " ".join(role_scopes)

        super().save_bearer_token(token, request, *args, **kwargs)
