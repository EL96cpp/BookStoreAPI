from django.shortcuts import render
from django.forms.models import model_to_dict
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
            serializer = CartSerializer(data=model_to_dict(cart))
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        data = request.data
        data._mutable = True
        data['customer'] = request.user.pk
        data['book'] = book_id

        serializer = CartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

    def delete(self, request):
        book_id = self.request.POST.get("book_id")
        cart = Cart.objects.filter(customer=self.request.user, book_id=book_id)
        if cart.exists():
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Book was not found in your cart!"}, status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self, request):
        quantity_update = int(self.request.POST.get("quantity_update"))
        book_id = self.request.POST.get("book_id")
        cart_query = Cart.objects.filter(customer=self.request.user, book_id=book_id)
        
        if not cart_query.exists():
            return Response({"message": "Book was not found in your cart!"}, status=status.HTTP_400_BAD_REQUEST)
        if quantity_update != 1 and quantity_update != -1:
            return Response({"message": "qunatity_update value must be 1 or -1"}, status=status.HTTP_400_BAD_REQUEST)

        cart = cart_query.first()
        
        if cart.quantity + quantity_update == 0:
            cart.delete()
            return Response({"message": "Book has been removed from your cart!"}, status=status.HTTP_200_OK)

        cart.quantity += quantity_update
        cart.save()
        serializer = CartSerializer(data=model_to_dict(cart), many=False)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)        
