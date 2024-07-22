from django.contrib import admin
from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["customer", "book", "quantity", "created_timestamp"]
    search_fields = ["customer", "book", "created_timestamp"]
