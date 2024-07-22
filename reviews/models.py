from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from books.models import Book
from customers.models import Customer


class Review(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, null=False, verbose_name="Книга")
    customer = models.ForeignKey(to=Customer, on_delete=models.PROTECT, null=False, verbose_name="Покупатель")
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0, verbose_name="Рейтинг")
    review = models.TextField(max_length=255, null=True, verbose_name="Отзыв")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"