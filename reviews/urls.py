from django.urls import path
from .views import *


urlpatterns = [
    path('add-review/<int:book_id>', BookCreateReviewView.as_view(), name="add-review"),
    path('book-reviews/<int:book_id>', BookReviewsListView.as_view(), name="book-review"),
    path('profile/reviews', CustomerReviewsListView.as_view(), name="customer-reviews"),
    path('profile/review/<int:pk>', CustomerReviewView.as_view(), name="customer-review"),
]
