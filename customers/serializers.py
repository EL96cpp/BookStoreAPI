from rest_framework import serializers
from .models import Customer

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CustomerSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserModel
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'needs_adverticing')


    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            needs_adverticing=validated_data['needs_adverticing']
        )
        return user