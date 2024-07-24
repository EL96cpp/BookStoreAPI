from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Customer
from django.contrib.auth import authenticate
from .serializers import CustomerSerializer

from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model


class CustomerLoginAPI(APIView):
    def post(self, request):
        print(request)
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)

        if user:
            return Response({'login': 'ok!'}, status=status.HTTP_200_OK)
        else:
            return Response({'login': 'incorrect data!'}, status=status.HTTP_401_UNAUTHORIZED)
        

class CreateUserView(CreateAPIView):
    model = get_user_model()
    serializer_class = CustomerSerializer