from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt_auth.managers import JWTTokenManager


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')  
        if not auth_header:
            return None
        try:
            header_parts = auth_header.split(' ')
            if len(header_parts) != 2 or header_parts[0].lower() != 'bearer':
                return None
            token = header_parts[1]
            user = JWTTokenManager.authenticate_by_access_token(token)
            return (user, token)
        except (ValueError, AuthenticationFailed):
            return None