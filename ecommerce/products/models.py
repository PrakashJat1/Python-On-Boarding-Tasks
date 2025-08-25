from django.db import models
from authentication.models import CustomUser
from main.utils import generate_unique_slug
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(default="", null=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.name)
            super().save(*args, **kwargs)

    # def get_url(self):
    #     return reverse("products-by-category", args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):

    # COLOR_CHOICE = [
    #     ("white", "White"),
    #     ("black", "Black"),
    #     ("red", "Red"),
    #     ("blue", "Blue"),
    #     ("green", "Green"),
    #     ("orange", "Orange"),
    #     ("yellow", "Yellow"),
    # ]
    # # CATEGORY_CHOICE = [
    #     ("fashion", "Fashion"),
    #     ("electronics", "Electronics"),
    #     ("home & kitchen", "Home & Kitchen"),
    #     ("beauty & personal car", "Beauty & Personal Care"),
    #     ("books", "Books"),
    #     ("toys", "Toys"),
    #     ("sports", "Sports"),
    # ]

    name = models.CharField(max_length=50)
    slug = models.SlugField(default="", null=False)
    price = models.PositiveBigIntegerField(default=0)
    quantity = models.PositiveBigIntegerField(default=0)
    seller = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="products"
    )
    image = models.ImageField(upload_to="products/")
    color = models.CharField(
        max_length=30,
        default="",
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    description = models.TextField(max_length=300, default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.name)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name
