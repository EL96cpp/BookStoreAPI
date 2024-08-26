from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from carts.models import Cart
from stores.models import Store
from books.models import Book
from customers.models import Customer
from orders.models import Order, OrderItem


class ReviewsTestView(APITestCase):

    def setUp(self):
        customer1 = Customer.objects.create(username="user1", password="qwerty1234qwerty",
                                            first_name="Joe", last_name="Simpson")
        customer2 = Customer.objects.create(username="user2", password="qwerty1234qwerty",
                                            first_name="Dan", last_name="Cooper")
    
        self.token_customer1 = Token.objects.create(user=customer1)
        self.token_customer2 = Token.objects.create(user=customer2)

        self.book1 = Book.objects.create(author="D.B.Cooper", title="Example title", price=2400.00, discount=0)
        self.book2 = Book.objects.create(author="N.B.Siemens", title="Example title2", price=1200.00, discount=50)
        self.book3 = Book.objects.create(author="H.J.Simpson", title="Example title3", price=500.00, discount=25)
        self.book4 = Book.objects.create(author="N.B.Siemens", title="Example title4", price=1100.00, discount=10)

        self.Store1 = Store.objects.create(city="Moscow", address="Example st., 10")
        self.Store2 = Store.objects.create(city="Moscow", address="Example 2 st., 5")


    def test_unauthorized_get_orders(self):
        response = self.client.get(reverse("orders"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_authorized_get_empty_orders(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer1.key)
        response = self.client.get(reverse("orders"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    
    def test_unauthorized_make_order(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer1.key)
        response1 = self.client.post(reverse("carts"), {"book_id": 1})
        response2 = self.client.post(reverse("carts"), {"book_id": 2})
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        self.client.logout()
        order_response = self.client.post(reverse("order"), {"store": 2, "payment_on_get": True})
        self.assertEqual(order_response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_authorized_make_order(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer1.key)
        response1 = self.client.post(reverse("carts"), {"book_id": 1})
        response2 = self.client.post(reverse("carts"), {"book_id": 2})
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        order_response = self.client.post(reverse("order"), {"store_id": 2, "payment_on_get": True})
        self.assertEqual(order_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(order_response.data["order_items"]), 2)
        self.assertEqual(order_response.data["order"]["customer"], 1)
        self.assertEqual(order_response.data["order"]["store"], 2)
        self.assertEqual(order_response.data["order"]["received"], False)
        self.assertEqual(order_response.data["order"]["payment_on_get"], True)
        self.assertEqual(order_response.data["order"]["is_paid"], False)
        self.assertEqual(order_response.data["order"]["status"], "В обработке")
        self.assertEqual(order_response.data["order"]["total"], 3000.00)
        self.assertEqual(order_response.data["order"]["books_quantity"], 2)

        carts_response = self.client.get(reverse("carts"))
        self.assertEqual(carts_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(carts_response.data), 0)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer2.key)
        order_response_client2 = self.client.get(reverse("orders"))
        self.assertEqual(order_response_client2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(order_response_client2.data), 0)
