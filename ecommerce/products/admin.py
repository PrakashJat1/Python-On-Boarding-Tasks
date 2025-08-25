from django.contrib import admin
from .models import Product, Category


class ProductAdminModel(admin.ModelAdmin):
    list_display = ["name", "price", "category", "quantity", "seller"]
    search_fields = ["name", "price", "category", "quantity", "seller"]


class CategoryAdminModel(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]


admin.site.register(Product, ProductAdminModel)
admin.site.register(Category, CategoryAdminModel)
