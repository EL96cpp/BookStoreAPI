from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Store
from .serializers import StoreSerializer


class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['city', 'address']
    filterset_fields = ['city',]

