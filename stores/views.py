from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Store
from .serializers import StoreSerializer
from django.http import JsonResponse


class StoreListView(ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['city', 'address']
    filterset_fields = ['city',]

    @method_decorator(cache_page(60*60*24))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)    

    class Meta:
        ordering = ['id']


