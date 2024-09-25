from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from books.views import *
from reviews.views import *
from carts.views import CartView
from orders.views import *
from stores.views import StoreListView
from .yasg import urlpatterns as doc_urls


router = SimpleRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include("books.urls")),
    path('api/v1/', include("reviews.urls")),
    path('api/v1/', include("carts.urls")),
    path('api/v1/', include("orders.urls")),
    path('api/v1/', include("stores.urls")),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]

urlpatterns += doc_urls
urlpatterns += router.urls
