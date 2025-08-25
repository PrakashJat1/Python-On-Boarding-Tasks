from django.contrib import admin
from .models import Order


class OrderAdminModel(admin.ModelAdmin):
    list_display = ["product", "customer", "status", "ordered_at"]
    search_fields = ["product", "customer"]


admin.site.register(Order, OrderAdminModel)
