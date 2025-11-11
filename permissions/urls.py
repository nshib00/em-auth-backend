from django.urls import include, path
from rest_framework.routers import DefaultRouter
from permissions.views import (
    PermissionViewSet,
    ActionViewSet,
    RoleViewSet,
    ResourceTypeViewSet
)

router = DefaultRouter()

viewsets_with_prefixes = [
    ('', PermissionViewSet),
    ('actions', ActionViewSet),
    ('roles', RoleViewSet),
    ('resourcetypes', ResourceTypeViewSet),
]

for prefix, viewset in viewsets_with_prefixes:
    router.register(prefix, viewset, basename=prefix)

urlpatterns = [
    path('', include(router.urls)),
]