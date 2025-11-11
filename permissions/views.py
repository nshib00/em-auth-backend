from rest_framework import viewsets, mixins
from permissions.models import Permission, Action, ResourceType, Role
from permissions.serializers import (
    PermissionSerializer,
    ActionSerializer,
    ResourceTypeSerializer,
    RoleSerializer
)
from permissions.classes import IsAdmin
from rest_framework.response import Response


class BasePermissionViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet
    ):
    permission_classes = [IsAdmin]

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PermissionViewSet(BasePermissionViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class ActionViewSet(BasePermissionViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class ResourceTypeViewSet(BasePermissionViewSet):
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer


class RoleViewSet(BasePermissionViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
