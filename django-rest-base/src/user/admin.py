from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import UserCredential
from base.admin import BaseAdmin
from . import models


@admin.register(models.User)
class UserAdmin(DefaultUserAdmin, BaseAdmin):
    list_display = ["id", "email", "name", "mobile_number"]
    list_filter = ["date_joined"]
    search_fields = ["email"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("name", "mobile_number")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "user_permissions",
                )
            },
        ),
    )

    ordering = ("id",)

@admin.register(UserCredential)
class UserCredentialAdmin(admin.ModelAdmin):
    list_display = ['user', 'access_key_id', 'secret_access_key', 'created_at']
    search_fields = ['user__email', 'access_key_id']