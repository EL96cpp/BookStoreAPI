from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    title = models.CharField(max_length=255, null=False, verbose_name="Название")
    author = models.CharField(max_length=255, null=False, verbose_name="Автор")
    price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2, null=False, verbose_name="Цена")
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(99)], default=0, null=True, verbose_name="Скидка")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        unique_together = ('title', 'author',)

    def sell_price(self):
        return round(self.price - (self.price*self.discount)/100, 2)
