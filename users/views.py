from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from jwt_auth.managers import JWTTokenManager
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

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
