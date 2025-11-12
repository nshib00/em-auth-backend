from rest_framework import viewsets, status
from rest_framework.response import Response
from mock_objects.serializers import MockOrderSerializer, MockProductSerializer
from permissions.classes import ResourceActionPermission
from mock_objects.objects import MOCK_ORDERS, MOCK_PRODUCTS


class BaseMockViewSet(viewsets.GenericViewSet):
    permission_classes = [ResourceActionPermission]
    resource_type = None
    resource_action = None

    def get_serializer_class(self):
        if self.resource_type == 'orders':
            return MockOrderSerializer
        elif self.resource_type == 'products':
            return MockProductSerializer
        return super().get_serializer_class()

    def get_mock_list(self):
        raise NotImplementedError()

    def get_mock_obj(self, pk):
        return next(
            (
                obj for obj in self.get_mock_list()
                if obj['id'] == int(pk)
            ),
            None
        )

    def list(self, request, *args, **kwargs):
        self.resource_action = 'view'
        return Response(self.get_mock_list())

    def retrieve(self, request, pk=None):
        self.resource_action = 'view'
        obj = self.get_mock_obj(pk)
        if obj is None:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(obj)

    def create(self, request, *args, **kwargs):
        self.resource_action = 'create'
        data = request.data
        self.get_mock_list().append(data)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        self.resource_action = 'change'
        obj = self.get_mock_obj(pk)
        if not obj:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        obj.update(request.data)
        return Response(obj)

    def destroy(self, request, pk=None, *args, **kwargs):
        self.resource_action = 'delete'
        obj = self.get_mock_obj(pk)
        if not obj:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        self.get_mock_list().remove(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MockOrderViewSet(BaseMockViewSet):
    resource_type = 'orders'
    serializer_class = MockOrderSerializer

    def get_mock_list(self):
        return MOCK_ORDERS


class MockProductViewSet(BaseMockViewSet):
    resource_type = 'products'

    def get_mock_list(self):
        return MOCK_PRODUCTS
