from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import views, mixins, permissions, status
from .models import Cart
from books.models import Book
from .serializers import CartSerializer


class CartView(views.APIView,
               mixins.ListModelMixin,
               mixins.CreateModelMixin):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Cart.objects.all()

    def get(self, request):
        carts = Cart.objects.filter(customer=request.user)
        return Response(CartSerializer(carts, many=True).data)

    
    def post(self, request):
        book_id = self.request.POST.get("book_id")
        cart_query = Cart.objects.filter(book_id=book_id, customer=self.request.user).all()
        if cart_query.exists():
            cart = cart_query.last()
            cart.quantity += 1
            cart.save()
            return Response(status=status.HTTP_200_OK)

        data = request.data
        data._mutable = True
        data['customer'] = request.user.pk
        data['book'] = book_id

        serializer = CartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)