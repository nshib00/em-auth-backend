from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from jwt_auth.managers import JWTTokenManager
from users.serializers import UserRegisterSerializer


class BaseUserView(GenericAPIView):
    user_model = get_user_model()


class UserRegisterView(GenericAPIView, CreateModelMixin):
    """View для регистрации пользователя"""
    serializer_class = UserRegisterSerializer
 
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        JWTTokenManager.create_token_pair(user_id=user.id)
        return Response(
            {
                'message': 'Registration successful',
                'user_id': user.id,
                'email': user.email,
            },
            status=status.HTTP_201_CREATED
        )
