from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from books.views import BookViewSet
from stores.views import StoreViewSet


router = SimpleRouter()
router.register(r"books", BookViewSet)
router.register(r"stores", StoreViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
