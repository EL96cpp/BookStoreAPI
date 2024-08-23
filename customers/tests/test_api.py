from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Customer


class CustomersApiTestCase(APITestCase):
    def setUp(self):
        self.client.post('/auth/users/', 
                        {"username": "username1", "password": "qwer1234qwer",
                        "first_name": "Joe", "last_name": "Simpson"})
    

    def test_customer_exists(self):
        customer = Customer.objects.filter(username="username1")
        self.assertEqual(customer[0].username, "username1")
        self.assertEqual(customer[0].first_name, "Joe")
        self.assertEqual(customer[0].last_name, "Simpson")


    def test_customer_token(self):
        response = self.client.post('/auth/token/login', 
                                    {"username": "username1", "password": "qwer1234qwer"})        
        token = response.data['auth_token']
        self.assertNotEqual(len(token), 0)


    def test_username_is_unique(self):
        response = self.client.post('/auth/users/', 
                                    {"username": "username1", "password": "qwer1234qwer",
                                    "first_name": "John", "last_name": "Simons"})        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
