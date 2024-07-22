from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from books.views import BookViewSet
from stores.views import StoreViewSet
from reviews.views import BookReviewsListView, CustomerReviewsListView


router = SimpleRouter()
router.register(r"books", BookViewSet)
router.register(r"stores", StoreViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('book-reviews/<int:book_id>', BookReviewsListView.as_view()),
    path('customer-reviews/<slug:username>', CustomerReviewsListView.as_view())
]

urlpatterns += router.urls
