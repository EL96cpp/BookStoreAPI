from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from carts.models import Cart
from books.models import Book
from customers.models import Customer


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


    def test_unauthorized_get_carts(self):
        response = self.client.get(reverse("carts"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_authorized_get_empty_carts(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer1.key)
        response = self.client.get(reverse("carts"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    
    def test_unauthorized_add_to_cart(self):
        response1 = self.client.post(reverse("carts"), {"book_id": 1})
        response2 = self.client.post(reverse("carts"), {"book_id": 2})
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_authorized_add_to_cart(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer1.key)
        response1 = self.client.post(reverse("carts"), {"book_id": 1})
        response2 = self.client.post(reverse("carts"), {"book_id": 2})
        self.assertEqual(response1.data['quantity'], 1)
        self.assertEqual(response1.data['book'], 1)
        self.assertEqual(response1.data['customer'], 1)
        self.assertEqual(response2.data['quantity'], 1)
        self.assertEqual(response2.data['book'], 2)
        self.assertEqual(response2.data['customer'], 1)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        response3 = self.client.post(reverse("carts"), {"book_id": 1})
        self.assertEqual(response3.data['quantity'], 2)
        self.assertEqual(response3.data['book'], 1)
        self.assertEqual(response3.data['customer'], 1)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)


    def test_authorized_get_carts(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer1.key)
        self.client.post(reverse("carts"), {"book_id": 2})
        self.client.post(reverse("carts"), {"book_id": 4})
        get_carts_response = self.client.get(reverse("carts"))
        self.assertEqual(get_carts_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(get_carts_response.data), 2)
        
        self.assertEqual(get_carts_response.data[0]["book"], 2)
        self.assertEqual(get_carts_response.data[0]["quantity"], 1)
        self.assertEqual(get_carts_response.data[1]["book"], 4)
        self.assertEqual(get_carts_response.data[1]["quantity"], 1)


    def test_increase_quantity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer1.key)
        response1 = self.client.post(reverse("carts"), {"book_id": 1})
        response2 = self.client.post(reverse("carts"), {"book_id": 2})
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        increase_response = self.client.patch(reverse("carts"), {"book_id": 1, "quantity_update": 1})
        self.assertEqual(increase_response.status_code, status.HTTP_200_OK)
        self.assertEqual(increase_response.data["book"], 1)
        self.assertEqual(increase_response.data["quantity"], 2)
        increase_response = self.client.patch(reverse("carts"), {"book_id": 1, "quantity_update": 1})
        self.assertEqual(increase_response.status_code, status.HTTP_200_OK)
        self.assertEqual(increase_response.data["book"], 1)
        self.assertEqual(increase_response.data["quantity"], 3)


    def test_decrease_quantity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer1.key)
        response1 = self.client.post(reverse("carts"), {"book_id": 3})
        response2 = self.client.post(reverse("carts"), {"book_id": 4})
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        self.client.patch(reverse("carts"), {"book_id": 3, "quantity_update": 1})
        self.client.patch(reverse("carts"), {"book_id": 3, "quantity_update": 1})
        self.client.patch(reverse("carts"), {"book_id": 4, "quantity_update": 1})
        self.client.patch(reverse("carts"), {"book_id": 4, "quantity_update": 1})

        decrease_response = self.client.patch(reverse("carts"), {"book_id": 3, "quantity_update": -1})
        self.assertEqual(decrease_response.status_code, status.HTTP_200_OK)
        self.assertEqual(decrease_response.data["book"], 3)
        self.assertEqual(decrease_response.data["quantity"], 2)
        decrease_response = self.client.patch(reverse("carts"), {"book_id": 4, "quantity_update": -1})
        self.assertEqual(decrease_response.status_code, status.HTTP_200_OK)
        self.assertEqual(decrease_response.data["book"], 4)
        self.assertEqual(decrease_response.data["quantity"], 2)


    def test_remove_from_cart(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer1.key)
        response1 = self.client.post(reverse("carts"), {"book_id": 3})
        response2 = self.client.post(reverse("carts"), {"book_id": 4})
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        remove_response = self.client.delete(reverse("carts"), {"book_id": 3})
        self.assertEqual(remove_response.status_code, status.HTTP_204_NO_CONTENT)

        get_carts_response = self.client.get(reverse("carts"))
        self.assertEqual(len(get_carts_response.data), 1)
        self.assertEqual(get_carts_response.data[0]["book"], 4)
        self.assertEqual(get_carts_response.data[0]["quantity"], 1)