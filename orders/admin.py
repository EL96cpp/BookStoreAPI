from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "store", "received", "ordered_timestamp", 
                    "received_timestamp", "payment_on_get", "status", "total"]
    list_filter = ["customer", "store", "received", "status"]
    search_fields = ["customer", "ordered_timestamp", "received_timestamp"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "book", "price", "quantity", "ordered_timestamp"]
    search_fields = ["order", "book",]


    