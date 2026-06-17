from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = [
        "id",
        "email",
        "first_name",
        "last_name",
        "registration_source",
        "phone_number",
        "birthday",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "registration_source",
                    "phone_number",
                    "birthday",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    ordering = ["email"]
