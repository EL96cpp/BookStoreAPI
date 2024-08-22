from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from stores.models import Store


class StoresTests(APITestCase):

    def setUp(self):
        Store.objects.create(city="Moscow", address="Example st., 9")
        Store.objects.create(city="Omsk", address="Example st., 15")


    def test_stores_list(self):
        response = self.client.get(reverse("stores"))
        
        expected_data = [
            {'id': 1, 'city': 'Moscow', 'address': 'Example st., 9'}, 
            {'id': 2, 'city': 'Omsk', 'address': 'Example st., 15'}
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    
    def test_city_filters(self):
        
        filter_moscow_response = self.client.get(reverse("stores"), {"city": "Moscow"})
        expected_filter_moscow_data = [
            {'id': 1, 'city': 'Moscow', 'address': 'Example st., 9'}, 
        ]
        self.assertEqual(filter_moscow_response.status_code, status.HTTP_200_OK)
        self.assertEqual(filter_moscow_response.data, expected_filter_moscow_data)

        filter_omsk_response = self.client.get(reverse("stores"), {"city": "Omsk"})
        expected_filter_omsk_data = [
            {'id': 2, 'city': 'Omsk', 'address': 'Example st., 15'},
        ]
        self.assertEqual(filter_omsk_response.status_code, status.HTTP_200_OK)
        self.assertEqual(filter_omsk_response.data, expected_filter_omsk_data)
