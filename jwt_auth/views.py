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
    ...


class TokensRefreshView(BaseUserView):
    ...
