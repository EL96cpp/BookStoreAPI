from orders.models import Order, OrderItem 
from carts.models import Cart
from books.models import Book
from stores.models import Store
from customers.models import Customer
from django.test import TestCase


class OrderTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(username="Username", password="qwerty", last_name="ln", first_name="fn")

        self.store = Store.objects.create(city="Moscow", address="Example st., 10")

        self.book1 = Book.objects.create(title="Title 1", author="Author 1", price=1250.10, discount=0)
        self.book2 = Book.objects.create(title="Title 2", author="Author 2", price=790.90, discount=10)
        self.book3 = Book.objects.create(title="Title 3", author="Author 1", price=400.00, discount=10)
        self.book4 = Book.objects.create(title="Title 4", author="Author 3", price=2000.00, discount=20)
        self.book5 = Book.objects.create(title="Title 5", author="Author 2", price=720.00, discount=50)
        
        self.book6 = Book.objects.create(title="Title 6", author="Author 4", price=1550.10, discount=0)
        self.book7 = Book.objects.create(title="Title 7", author="Author 4", price=750.90, discount=10)
        self.book8 = Book.objects.create(title="Title 8", author="Author 4", price=460.00, discount=5)
        self.book9 = Book.objects.create(title="Title 9", author="Author 2", price=2400.00, discount=15)
        self.book10 = Book.objects.create(title="Title 10", author="Author 2", price=1420.00, discount=0)

        self.cart1 = Cart.objects.create(book=self.book1, customer=self.customer, quantity=2)
        self.cart2 = Cart.objects.create(book=self.book3, customer=self.customer, quantity=3)
        self.cart3 = Cart.objects.create(book=self.book4, customer=self.customer, quantity=4)
        self.cart4 = Cart.objects.create(book=self.book7, customer=self.customer, quantity=5)
        self.cart5 = Cart.objects.create(book=self.book9, customer=self.customer, quantity=1)


    def test_order(self):
        
        carts_query = Cart.objects.filter(customer=self.customer)

        self.order1 = Order.objects.create(customer=self.customer, store=self.store, 
                                           payment_on_get=False, total=carts_query.total_price(),
                                           books_quantity=carts_query.total_quantity())

        self.assertEqual(self.order1.total, 15399.25)
        self.assertEqual(self.order1.books_quantity, 15)
        self.assertEqual(self.order1.status, 'В обработке')
        self.assertEqual(self.order1.received, False)