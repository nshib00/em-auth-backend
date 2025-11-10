from rest_framework.response import Response
from rest_framework import status
from auth_backend.views import BaseUserView
from jwt_auth.managers import JWTTokenManager
from jwt_auth.serializers import LoginSerializer


class LoginView(BaseUserView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = self.user_model.objects.get(email=email)
            if user.check_password(password) and user.is_active:
                tokens = JWTTokenManager.create_token_pair(user.pk) 
                return Response({
                    'user_id': user.pk,
                    'email': user.email,
                    'access_token': tokens.access_token,
                    'refresh_token': tokens.refresh_token,
                })
            else:
                return Response(
                    {'error': 'Invalid credentials or inactive account'},
                    status=status.HTTP_401_UNAUTHORIZED
                )   
        except self.user_model.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(BaseUserView):
    def post(self, request):
        auth_header = request.headers.get('Authorization', '')
        access_token = None
        
        token_parts = auth_header.split(' ')
        if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
            return Response(
                {'message': 'Invalid user token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        access_token = auth_header.split(' ')[1]
        
        JWTTokenManager.delete_user_refresh_tokens(request.user.id)
        if access_token:
            JWTTokenManager.blacklist_token(access_token)
        return Response({
            'message': 'Successfully logged out.'
        })


class TokensRefreshView(BaseUserView):
    ...
