from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from books.views import *
from stores.views import StoreViewSet
from reviews.views import *
from customers.views import CustomerLoginAPI, CreateUserView
from .yasg import urlpatterns as doc_urls


router = SimpleRouter()
router.register(r"api/v1/books", BookListViewSet)
router.register(r"api/v1/stores", StoreViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/book/<int:pk>', BookDetailView.as_view()),
    path('api/v1/add-review/<int:book_id>', BookCreateReviewView.as_view()),
    path('api/v1/book-reviews/<int:book_id>', BookReviewsListView.as_view()),
    path('api/v1/profile/reviews/', CustomerReviewsListView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]

urlpatterns += doc_urls

urlpatterns += router.urls
