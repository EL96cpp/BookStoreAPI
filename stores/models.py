from django.db import models

class Store(models.Model):
    city = models.CharField(max_length=255, null=False, verbose_name="Город")
    address = models.CharField(max_length=255, null=False, verbose_name="Адрес")

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"