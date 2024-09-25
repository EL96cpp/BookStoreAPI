from django.urls import path
from .views import *


urlpatterns = [
    path('orders', OrderListView.as_view(), name="orders"),
    path('order/<int:order_id>', OrderRetrieveView.as_view(), name="order"),
    path('order', OrderCreateView.as_view(), name="order")
]