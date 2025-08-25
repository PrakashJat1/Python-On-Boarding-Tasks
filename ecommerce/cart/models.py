from django.db import models
from authentication.models import CustomUser
from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="cart")

    def __str__(self):
        return self.user.first_name 


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.cart.user.first_name
    
    
class WishList(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="wishlist")
    products = models.ManyToManyField(Product, related_name="wishlist")

    def __str__(self):
        return self.user.first_name    
