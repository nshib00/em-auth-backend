from django.urls import include, path
from rest_framework.routers import DefaultRouter

from mock_objects.views import MockOrderViewSet, MockProductViewSet


router = DefaultRouter()
router.register('orders', MockOrderViewSet, basename='orders')
router.register('products', MockProductViewSet, basename='products')


urlpatterns = [
    path('', include(router.urls)),
]
