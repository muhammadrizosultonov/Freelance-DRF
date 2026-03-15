from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["id", "username", "email", "role", "created_at", "is_staff"]
    list_filter = ["role", "is_staff", "is_superuser"]
    fieldsets = UserAdmin.fieldsets + (
        ("Extra", {"fields": ("role", "bio", "created_at")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra", {"fields": ("role", "bio")}),
    )
    readonly_fields = ["created_at"]
