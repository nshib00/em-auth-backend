from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from jwt_auth.managers import JWTTokenManager
from jwt_auth.utils import get_access_token_from_request
from users.serializers import UserProfileSerializer, UserRegisterSerializer


class UserRegisterView(GenericAPIView, CreateModelMixin):
    serializer_class = UserRegisterSerializer
 
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = JWTTokenManager.create_token_pair(user_id=user.id)
        return Response(
            {
                'user_id': user.id,
                'email': user.email,
                'tokens': {
                    'access': tokens.access_token,
                    'refresh': tokens.refresh_token
                }
            },
            status=status.HTTP_201_CREATED
        )
    

class UserProfileView(GenericAPIView, UpdateModelMixin, DestroyModelMixin):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request):
        user = self.get_object()
        user_id = user.pk
        user.delete()
        access_token = get_access_token_from_request(request)
        if access_token is None:
            return Response(
                {'message': 'No token provided or token is invalid.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        JWTTokenManager.blacklist_token(access_token)
        JWTTokenManager.delete_user_refresh_tokens(user_id=user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_object(self):
        return self.request.user
