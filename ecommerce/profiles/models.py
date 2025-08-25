from django.db import models
from authentication.models import CustomUser


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    profile_picture = models.ImageField(upload_to="profiles", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class Address(models.Model):
    address_name = models.CharField(max_length=500, editable=False, blank=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="address"
    )
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.address_name = (
            f"{self.street}, {self.city}, {self.state}, {self.zip_code}, {self.country}"
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.address_name
