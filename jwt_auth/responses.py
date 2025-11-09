from django.http import JsonResponse
from django.conf import settings


class AccessTokenResponse(JsonResponse):
    '''Response, работающий с куками access токена'''
    
    def set_access_token_cookie(self, access_token: str):
        self.set_cookie(
            'em_access_token',
            access_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=900,
            path='/'
        )
    
    def clear_access_token_cookie(self):
        self.delete_cookie('access_token')