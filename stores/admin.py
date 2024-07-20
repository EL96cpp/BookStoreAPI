from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["city", "address"]
    list_filter = ["city",]
    search_fields = ["address",]
    ordering = ["city",]

