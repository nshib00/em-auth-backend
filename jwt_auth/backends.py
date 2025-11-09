from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt_auth.managers import JWTTokenManager


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('em_access_token')
        if not access_token:
            return None
        
        try:
            user = JWTTokenManager.authenticate_by_access_token(access_token)
            return (user, None)       
        except AuthenticationFailed as e:
            raise e
