from rest_framework.serializers import ModelSerializer
from .models import Cart
from books.serializers import BookSerializer


class CartSerializer(ModelSerializer):
    book = BookSerializer(many=False)

    class Meta:
        model = Cart
        fields = '__all__'