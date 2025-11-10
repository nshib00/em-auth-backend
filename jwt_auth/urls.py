from django.urls import path

from jwt_auth.views import LoginView, LogoutView, TokensRefreshView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('refresh/', TokensRefreshView.as_view(), name='tokens-refresh'),
]