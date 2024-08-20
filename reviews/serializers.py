from rest_framework.serializers import ModelSerializer
from .models import Review


class ReviewCreateSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'review']

    

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'