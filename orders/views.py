from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework import views, generics, mixins, permissions, status
from .models import Order, OrderItem
from carts.models import Cart
from books.models import Book
from stores.models import Store
from .serializers import OrderSerializer, OrderItemSerializer
from .tasks import send_order_email

from django.conf import settings


class OrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,] 
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
    
    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)    



class OrderRetrieveView(views.APIView):
    permission_classes = [permissions.IsAuthenticated,]

    @method_decorator(cache_page(60))
    def get(self, request, order_id):
        order = Order.objects.filter(id=order_id, customer=request.user)
        if not order.exists():
            return Response({"message": "Order not found!"}, status=status.HTTP_404_NOT_FOUND)
        order_items = OrderItem.objects.filter(order_id=order_id)    
        return Response({"order": OrderSerializer(order.first(), many=False).data,
                         "order-items": OrderItemSerializer(order_items.all(), many=True).data})


class OrderCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        carts_query = Cart.objects.filter(customer=request.user)
        if not carts_query.exists():
            return Response({"message": "Your cart is empty! Add books to your cart to make order!"}, 
                            status=status.HTTP_403_FORBIDDEN)
        carts = carts_query.all()
        store_id = int(request.POST.get("store_id"))
        payment_on_get = bool(request.POST.get("payment_on_get"))
        order = Order(customer=request.user, 
                      store_id=store_id, 
                      payment_on_get=payment_on_get,
                      total=carts_query.total_price(),
                      books_quantity=carts_query.total_quantity())
        order.save()
        order_items = []
        books = []
        for cart in carts:
            book = dict()
            book['title'] = cart.book.title
            book['author'] = cart.book.author
            book['price'] = cart.book.price
            book['quantity'] = cart.quantity
            books.append(book)
            order_item = OrderItem(order=order, book=cart.book, 
                                   price=cart.total_price(), quantity=cart.quantity)
            order_items.append(order_item)
            order_item.save()
        carts.delete()
        order_items = OrderItem.objects.filter(order=order)
        store = Store.objects.filter(id=store_id).last()
        send_order_email(settings.EMAIL_HOST_USER, request.user.email, store.city+", "+store.address, 
                         books, carts_query.total_price())
        return Response({"order": model_to_dict(order), 
                         "order_items": OrderItemSerializer(order_items, many=True).data},
                        status=status.HTTP_201_CREATED)