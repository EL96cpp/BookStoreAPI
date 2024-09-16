from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book
from .paginators import BookListPaginator
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    pagination_class = BookListPaginator
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', 'author']
    filterset_fields = ['price', 'discount']
    ordering_fields = ['title', 'price', 'discount']

    @method_decorator(cache_page(30*60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @method_decorator(cache_page(30*60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)