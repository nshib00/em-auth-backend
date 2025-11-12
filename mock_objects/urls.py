from django.urls import include, path
from mock_objects.views import (
    OrdersListView, OrdersRetrieveView, OrdersCreateView,
    OrdersUpdateView, OrdersDeleteView,
    ProductsListView, ProductsRetrieveView, ProductsCreateView,
    ProductsUpdateView, ProductsDeleteView
)

order_urls = [
    path('', OrdersListView.as_view()),
    path('create/', OrdersCreateView.as_view()),
    path('<int:pk>/', OrdersRetrieveView.as_view()),
    path('<int:pk>/update/', OrdersUpdateView.as_view()),
    path('<int:pk>/delete/', OrdersDeleteView.as_view()),
]

product_urls = [
    path('', ProductsListView.as_view()),
    path('create/', ProductsCreateView.as_view()),
    path('<int:pk>/', ProductsRetrieveView.as_view()),
    path('<int:pk>/update/', ProductsUpdateView.as_view()),
    path('<int:pk>/delete/', ProductsDeleteView.as_view()),
]

urlpatterns = [
    path('orders/', include(order_urls)),
    path('products/', include(product_urls)),
]
