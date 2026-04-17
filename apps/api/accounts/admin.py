from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Profile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):  # type: ignore[type-arg]
    list_display = ("username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("id", "user", "display_name", "created_at")
    search_fields = ("display_name", "user__username", "user__email")
    raw_id_fields = ("user",)
