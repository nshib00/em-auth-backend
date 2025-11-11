from rest_framework import viewsets, mixins
from permissions.models import Permission
from permissions.serializers import PermissionSerializer
from permissions.classes import IsAdmin
from rest_framework.response import Response


class PermissionViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.CreateModelMixin,
        viewsets.GenericViewSet
    ):
    permission_classes = [IsAdmin]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
