from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book


class BooksApiTestCase(APITestCase):
    def setUp(self):
        Book.objects.create(title="Title 1", author="Author 1", price=1250.10, discount=0)
        Book.objects.create(title="Title 2", author="Author 2", price=790.90, discount=10)
        Book.objects.create(title="Title 3", author="Author 1", price=490.00, discount=5)
        Book.objects.create(title="Title 4", author="Author 3", price=2200.00, discount=15)
        Book.objects.create(title="Title 5", author="Author 2", price=720.00, discount=0)
        
        Book.objects.create(title="Title 6", author="Author 4", price=1550.10, discount=0)
        Book.objects.create(title="Title 7", author="Author 4", price=750.90, discount=10)
        Book.objects.create(title="Title 8", author="Author 4", price=460.00, discount=5)
        Book.objects.create(title="Title 9", author="Author 2", price=2400.00, discount=15)
        Book.objects.create(title="Title 10", author="Author 2", price=1420.00, discount=0)
        
        Book.objects.create(title="Title 11", author="Author 1", price=1450.10, discount=0)
        Book.objects.create(title="Title 12", author="Author 1", price=795.90, discount=10)
        Book.objects.create(title="Title 13", author="Author 3", price=1550.00, discount=5)
        Book.objects.create(title="Title 14", author="Author 3", price=2520.00, discount=15)
        Book.objects.create(title="Title 15", author="Author 3", price=2550.00, discount=0)

        Book.objects.create(title="Title 16", author="Author 1", price=1330.10, discount=0)
        Book.objects.create(title="Title 17", author="Author 1", price=793.90, discount=10)
        Book.objects.create(title="Title 18", author="Author 3", price=1520.00, discount=5)
        Book.objects.create(title="Title 19", author="Author 3", price=3250.00, discount=15)
        Book.objects.create(title="Title 20", author="Author 3", price=1555.00, discount=0)

        Book.objects.create(title="Title 21", author="Author 5", price=1570.00, discount=0)


    def test_get(self):
        response = self.client.get(reverse('book-list'))
        data = response.data['results']

        first_page_expected = [
            {'id': 1, 'title': 'Title 1', 'author': 'Author 1', 'price': '1250.10', 'discount': 0},
            {'id': 2, 'title': 'Title 2', 'author': 'Author 2', 'price': '790.90', 'discount': 10},
            {'id': 3, 'title': 'Title 3', 'author': 'Author 1', 'price': '490.00', 'discount': 5},
            {'id': 4, 'title': 'Title 4', 'author': 'Author 3', 'price': '2200.00', 'discount': 15},
            {'id': 5, 'title': 'Title 5', 'author': 'Author 2', 'price': '720.00', 'discount': 0},
            {'id': 6, 'title': 'Title 6', 'author': 'Author 4', 'price': '1550.10', 'discount': 0},
            {'id': 7, 'title': 'Title 7', 'author': 'Author 4', 'price': '750.90', 'discount': 10},
            {'id': 8, 'title': 'Title 8', 'author': 'Author 4', 'price': '460.00', 'discount': 5},
            {'id': 9, 'title': 'Title 9', 'author': 'Author 2', 'price': '2400.00', 'discount': 15},
            {'id': 10, 'title': 'Title 10', 'author': 'Author 2', 'price': '1420.00', 'discount': 0}
        ]
        second_page_expected = [
            {'id': 11, 'title': 'Title 11', 'author': 'Author 1', 'price': '1450.10', 'discount': 0},
            {'id': 12, 'title': 'Title 12', 'author': 'Author 1', 'price': '795.90', 'discount': 10},
            {'id': 13, 'title': 'Title 13', 'author': 'Author 3', 'price': '1550.00', 'discount': 5},
            {'id': 14, 'title': 'Title 14', 'author': 'Author 3', 'price': '2520.00', 'discount': 15},
            {'id': 15, 'title': 'Title 15', 'author': 'Author 3', 'price': '2550.00', 'discount': 0},
            {'id': 16, 'title': 'Title 16', 'author': 'Author 1', 'price': '1330.10', 'discount': 0},
            {'id': 17, 'title': 'Title 17', 'author': 'Author 1', 'price': '793.90', 'discount': 10},
            {'id': 18, 'title': 'Title 18', 'author': 'Author 3', 'price': '1520.00', 'discount': 5},
            {'id': 19, 'title': 'Title 19', 'author': 'Author 3', 'price': '3250.00', 'discount': 15},
            {'id': 20, 'title': 'Title 20', 'author': 'Author 3', 'price': '1555.00', 'discount': 0}            
        ]
        third_page_expected = [
            {'id': 21, 'title': 'Title 21', 'author': 'Author 5', 'price': '1570.00', 'discount': 0},
        ]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(10, len(data))
        self.assertEqual(first_page_expected, data)

        second_page_response = self.client.get(reverse('book-list'), {"page": 2})
        second_page_data = second_page_response.data['results']

        self.assertEqual(10, len(second_page_data))
        self.assertEqual(second_page_expected, second_page_data)

        third_page_response = self.client.get(reverse('book-list'), {"page": 3})
        third_page_data = third_page_response.data['results']

        self.assertEqual(1, len(third_page_data))
        self.assertEqual(third_page_expected, third_page_data)

