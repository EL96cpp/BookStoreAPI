from rest_framework.serializers import ModelSerializer
from .models import Review
from books.serializers import BookSerializer


class ReviewCreateSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'review']

    
class ReviewSerializer(ModelSerializer):
    book = BookSerializer(many=False)

    class Meta:
        model = Review
        fields = '__all__'


class ReviewRetrieveUpdateSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {
            'review_id': {'read_only': True},
            'book': {'read_only': True},
            'customer': {'read_only': True},
            'rating': {'read_only': False},
            'review': {'read_only': False} 
        }