from django.contrib import admin
from .models import Cart, CartItem, WishList


class CartAdminModel(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user"]


class CartItemAdminModel(admin.ModelAdmin):
    list_display = ["cart", "product", "quantity"]
    search_fields = ["cart", "product", "quantity"]


class WishListAdminModel(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user"]


admin.site.register(Cart, CartAdminModel)
admin.site.register(CartItem, CartItemAdminModel)
admin.site.register(WishList, WishListAdminModel)
