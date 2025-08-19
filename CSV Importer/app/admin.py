from django.contrib import admin
from .models import User


class UserAdminModel(admin.ModelAdmin):
    search_fields = ["name", "age", "phone_no"]
    list_display = ["name", "age", "phone_no"]


admin.site.register(User, UserAdminModel)
