from django.urls import path
from .views import *


urlpatterns = [
    path('stores', StoreListView.as_view(), name="stores"),
]