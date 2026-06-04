from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ConfirmationCode
from users.models import CustomUser

admin.site.register(ConfirmationCode)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["id", "email", "phone_number", "is_active"]
    fieldsets = (
        (None, {"fields": ("email", "password", "phone_number", "is_active")}),
        ("important dates", {"fields": ("last_login",)}),
    )
    ordering = ["email"]
