from books.models import Book
from books.serializers import BookSerializer
from django.test import TestCase


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create(title="Title 1", author="Author 1", price=1250.10, discount=0)
        self.book2 = Book.objects.create(title="Title 2", author="Author 2", price=790.90, discount=10)

    def test_book_serializer(self):
        data = BookSerializer([self.book1, self.book2], many=True).data
        expected_data = [
            {
                'id': self.book1.id,
                'title': "Title 1",
                'author': "Author 1",
                'price': '1250.10',
                'discount': 0
            },
            {
                'id': self.book2.id,
                'title': "Title 2",
                'author': "Author 2",
                'price': '790.90',
                'discount': 10
            }
        ]
        self.assertEqual(expected_data, data)
