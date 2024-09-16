from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import generics, views
from rest_framework import permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import ReviewSerializer, ReviewCreateSerializer
from .models import Review
from .paginators import *
from books.models import Book


class BookReviewsListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = BookReviewsPaginator

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Review.objects.filter(book_id=book_id)
    
    @method_decorator(cache_page(60*30))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)    


class BookCreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Review.objects.all()
    
    def perform_create(self, serializer, book_id):
        book = Book.objects.filter(id=book_id).last()
        return serializer.save(customer=self.request.user, book=book)
    
    def create(self, request, *args, **kwargs):
        book_id = kwargs['book_id']
        if Review.objects.filter(book_id=book_id, customer=self.request.user).exists():
            return Response({"message": "You've already made reviewe on this book!"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer, book_id)
        headers = self.get_success_headers(serializer.data)
        serializer = ReviewSerializer(instance=instance, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomerReviewsListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated,]
    pagination_class = CustomerReviewsPaginator

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(customer=user)
    
    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)    