from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ConfirmationCode
from users.models import CustomUser

admin.site.register(ConfirmationCode)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["id", "email", "is_active"]
    fieldsets = (
        (None, {"fields": ("email", "password", "is_active")}),
        ("important dates", {"fields": ("last_login",)}),
    )
    ordering = ["email"]
