from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from permissions.classes import ResourceActionPermission
from mock_objects.objects import MOCK_ORDERS, MOCK_PRODUCTS
from mock_objects.serializers import MockOrderSerializer, MockProductSerializer


class BaseMockAPIView(APIView):
    permission_classes = [ResourceActionPermission]
    resource_type = None
    resource_action = None
    serializer_class = None

    def get_mock_list(self):
        raise NotImplementedError()

    def get_mock_obj(self, pk):
        try:
            pk = int(pk)
        except (TypeError, ValueError):
            return None
        return next((obj for obj in self.get_mock_list() if obj['id'] == pk), None)
    

class BaseMockOrdersView(BaseMockAPIView):
    serializer_class = MockOrderSerializer

    def get_mock_list(self):
        return MOCK_ORDERS
    

class BaseMockProductsView(BaseMockAPIView):
    serializer_class = MockProductSerializer
    
    def get_mock_list(self):
        return MOCK_PRODUCTS


class OrdersListView(BaseMockOrdersView):
    resource_type = 'orders'
    resource_action = 'view'
    

    def get(self, request):
        serializer = self.serializer_class(self.get_mock_list(), many=True)
        return Response(serializer.data)


class OrdersRetrieveView(BaseMockOrdersView):
    resource_type = 'orders'
    resource_action = 'view'
    
    def get(self, request, pk):
        obj = self.get_mock_obj(pk)
        if obj is None:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)


class OrdersCreateView(BaseMockOrdersView):
    resource_type = 'orders'
    resource_action = 'create'

    def post(self, request):
        data = request.data
        self.get_mock_list().append(data)
        return Response(data, status=status.HTTP_201_CREATED)


class OrdersUpdateView(BaseMockOrdersView):
    resource_type = 'orders'
    resource_action = 'change'

    def put(self, request, pk):
        obj = self.get_mock_obj(pk)
        if not obj:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        obj.update(request.data)
        return Response(obj)


class OrdersDeleteView(BaseMockOrdersView):
    resource_type = 'orders'
    resource_action = 'delete'

    def delete(self, request, pk):
        obj = self.get_mock_obj(pk)
        if not obj:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        self.get_mock_list().remove(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductsListView(BaseMockProductsView):
    resource_type = 'products'
    resource_action = 'view'

    def get(self, request):
        serializer = self.serializer_class(self.get_mock_list(), many=True)
        return Response(serializer.data)


class ProductsRetrieveView(BaseMockProductsView):
    resource_type = 'products'
    resource_action = 'view'

    def get(self, request, pk):
        obj = self.get_mock_obj(pk)
        if obj is None:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)


class ProductsCreateView(BaseMockProductsView):
    resource_type = 'products'
    resource_action = 'create'

    def post(self, request):
        data = request.data
        self.get_mock_list().append(data)
        return Response(data, status=status.HTTP_201_CREATED)


class ProductsUpdateView(BaseMockProductsView):
    resource_type = 'products'
    resource_action = 'change'

    def put(self, request, pk):
        obj = self.get_mock_obj(pk)
        if not obj:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        obj.update(request.data)
        return Response(obj)


class ProductsDeleteView(BaseMockProductsView):
    resource_type = 'products'
    resource_action = 'delete'

    def delete(self, request, pk):
        obj = self.get_mock_obj(pk)
        if not obj:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        self.get_mock_list().remove(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)
