from django.db import models
from django.core.validators import MinValueValidator
from customers.models import Customer
from books.models import Book


class CartQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.total_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, null=False, verbose_name="Клиент")
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, null=False, verbose_name="Книга")
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1),], null=False, verbose_name="Количество")
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'cart'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        ordering = ("id",)

    objects = CartQueryset().as_manager()

    def total_price(self):
        return round(self.book.sell_price() * self.quantity, 2)