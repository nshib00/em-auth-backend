from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.auth.token_manager import JWTTokenManager


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None  
        try:
            scheme, token_key = auth_header.split(' ')
            if scheme.lower() != 'bearer':
                return None    
            jwt_manager = JWTTokenManager()
            user = jwt_manager.authenticate_by_access_token(token_key)
            if not user:
                raise AuthenticationFailed('Invalid or expired token')   
            return (user, None)   
        except (IndexError, ValueError):
            raise AuthenticationFailed('Incorrect token format')
