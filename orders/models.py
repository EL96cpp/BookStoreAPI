from django.db import models
from books.models import Book
from customers.models import Customer
from stores.models import Store


class OrderitemQueryset(models.QuerySet):    
    def total_price(self):
        return sum(book.products_price() for book in self)


    def total_quantity(self):
        if self:
            return sum(book.quantity for book in self)
        return 0


class Order(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.PROTECT, null=False, verbose_name="Клиент")
    store = models.ForeignKey(to=Store, on_delete=models.PROTECT, null=False, verbose_name="Магазин")
    received = models.BooleanField(null=False, default=False, verbose_name="Получен")
    ordered_timestamp = models.DateTimeField(null=False, auto_now_add=True, verbose_name="Дата оформления")
    received_timestamp = models.DateTimeField(null=True, verbose_name="Дата получения")
    payment_on_get = models.BooleanField(default=False, verbose_name="Оплата при получении")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.CharField(max_length=50, default='В обработке', verbose_name="Статус заказа")
    total = models.IntegerField(default=0, verbose_name="Сумма заказа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("id",)

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.customer.first_name} {self.customer.last_name}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    book = models.ForeignKey(to=Book, on_delete=models.SET_DEFAULT, null=True, verbose_name="Цена", default=None)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    ordered_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")

    class Meta:
        db_table = "order_item"
        verbose_name = "Заказанная книга"
        verbose_name_plural = "Заказанные книги"
        ordering = ("id",)

    objects = OrderitemQueryset.as_manager()

    def item_price(self):
        print(round(self.book.sell_price() * self.quantity, 2), "order item ", self.book)
        return round(self.book.sell_price() * self.quantity, 2)


    def __str__(self):
        return f"Товар {self.book} | Заказ № {self.order.pk}"
    