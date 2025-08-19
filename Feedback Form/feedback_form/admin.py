from django.contrib import admin
from .models import Feedback

# Register your models here.


class FeedbackAdminModel(admin.ModelAdmin):
    search_fields = ("username", "email")
    list_display = ("username", "email", "feedback")


admin.site.register(Feedback, FeedbackAdminModel)
