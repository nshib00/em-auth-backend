from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt_auth.managers import JWTTokenManager


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')  
        if not auth_header:
            return None
        try:
            scheme, token = auth_header.split(' ')
            if scheme.lower() != 'bearer':
                return None
            user = JWTTokenManager.authenticate_by_access_token(token)
            return (user, None)
        except (ValueError, AuthenticationFailed):
            return None