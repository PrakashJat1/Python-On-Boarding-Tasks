from django.db import models
from authentication.models import CustomUser
from products.models import Product
from datetime import datetime
from django.utils import timezone


class Order(models.Model):

    ORDER_STATUS_CHOICE = [
        ("on the way", "On the way"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
        ("returned", "Returned"),
    ]

    ORDER_PAYMENT_STATUS_CHOICE = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("rejected", "Rejected"),
    ]

    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="orders"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="orders"
    )
    quantity = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=255, default="")
    payment_mode = models.CharField(max_length=40, blank=True, null=True)
    payment_status = models.BooleanField(default=False, blank=True)
    status = models.CharField(
        max_length=10, default="on the Way", choices=ORDER_STATUS_CHOICE
    )
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    ordered_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.product.name
