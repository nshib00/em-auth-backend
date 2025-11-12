from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


api_urls = [
    path('users/', include('users.urls')),
    path('auth/', include('jwt_auth.urls')),
    path('permissions/', include('permissions.urls')),
    path('objects/', include('mock_objects.urls')),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]