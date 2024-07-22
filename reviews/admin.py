from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["book", "customer", "rating", "review"]
    list_filter = ["book", "customer", "rating"]
    search_fields = ["book", "customer", "review"]
