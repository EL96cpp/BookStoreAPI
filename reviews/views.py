from rest_framework import generics
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .serializers import ReviewSerializer
from .models import Review
from .paginators import *
from books.models import Book


class BookReviewsListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = BookReviewsPaginator

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Review.objects.filter(book_id=book_id)


class BookCreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer




class CustomerReviewsListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated,]
    pagination_class = CustomerReviewsPaginator

    def get_queryset(self):
        user = self.request.user
        print(user.username)
        return Review.objects.filter(customer=user)