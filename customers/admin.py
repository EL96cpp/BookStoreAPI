from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name"]
    search_fields = ["username", "first_name", "last_name"]
