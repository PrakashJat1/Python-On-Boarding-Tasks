from django.contrib import admin
from .models import Profile, Address


class ProfileAdminModel(admin.ModelAdmin):
    list_display = ["user__first_name", "bio", "dob"]
    search_fields = ["user__first_name", "bio", "dob"]


class AdressAdminModel(admin.ModelAdmin):
    list_display = ["user__first_name", "address_name"]
    search_fields = ["user__first_name", "address_name"]


admin.site.register(Profile, ProfileAdminModel)
admin.site.register(Address, AdressAdminModel)
