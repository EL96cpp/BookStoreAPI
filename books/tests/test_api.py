from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book


class BooksApiTestCase(APITestCase):
    def setUp(self):
        book1 = Book.objects.create(title="Title 1", author="Author 1", price=1250.10, discount=0)
        book2 = Book.objects.create(title="Title 2", author="Author 2", price=790.90, discount=10)
        book3 = Book.objects.create(title="Title 3", author="Author 1", price=490.00, discount=5)
        book4 = Book.objects.create(title="Title 4", author="Author 3", price=2200.00, discount=15)
        book5 = Book.objects.create(title="Title 5", author="Author 2", price=720.00, discount=0)

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)