from django.contrib import admin
from .models import CustomUser, EmailTemplate


class UserAdminModel(admin.ModelAdmin):
    list_display = ["first_name", "email", "role", "is_active"]
    search_fields = ["first_name", "last_name", "email"]


class EmailTemplateAdminModel(admin.ModelAdmin):
    list_display = ["identifier", "template"]
    search_fields = ["identifier"]


admin.site.register(EmailTemplate, EmailTemplateAdminModel)


admin.site.register(CustomUser, UserAdminModel)
