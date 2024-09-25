from django.urls import path
from .views import *


urlpatterns = [
    path('book/<int:pk>', BookDetailView.as_view(), name="book"),
    path('book-list', BookListView.as_view(), name="book-list"),
]