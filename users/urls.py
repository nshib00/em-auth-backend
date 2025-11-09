from django.urls import path

from users.views import UserProfileView, UserRegisterView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('me/', UserProfileView.as_view(), name='profile'),
]