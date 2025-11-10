from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView


class BaseUserView(GenericAPIView):
    user_model = get_user_model()
