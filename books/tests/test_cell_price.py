from books.models import Book
from django.test import TestCase


class BookSellPriceTestCase(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create(title="Title 1", author="Author 1", price=1250.10, discount=0)
        self.book2 = Book.objects.create(title="Title 2", author="Author 2", price=790.90, discount=10)
        self.book3 = Book.objects.create(title="Title 3", author="Author 3", price=2300.00, discount=15)
        self.book4 = Book.objects.create(title="Title 4", author="Author 4", price=2540.00, discount=30)
        self.book5 = Book.objects.create(title="Title 5", author="Author 5", price=1420.20, discount=50)


    def test_book_sell_price(self):
        self.assertEqual(self.book1.sell_price(), self.book1.price)
        self.assertEqual(self.book2.sell_price(), round(self.book2.price - self.book2.price*self.book2.discount/100, 2))
        self.assertEqual(self.book3.sell_price(), round(self.book3.price - self.book3.price*self.book3.discount/100, 2))
        self.assertEqual(self.book4.sell_price(), round(self.book4.price - self.book4.price*self.book4.discount/100, 2))
        self.assertEqual(self.book5.sell_price(), round(self.book5.price - self.book5.price*self.book5.discount/100, 2))