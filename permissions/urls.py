from django.urls import include, path
from rest_framework.routers import DefaultRouter
from permissions.views import PermissionViewSet

router = DefaultRouter()
router.register('', PermissionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

