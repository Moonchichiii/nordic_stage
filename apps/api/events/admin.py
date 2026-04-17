from django.contrib import admin

from events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin[Event]):
    list_display = (
        "name",
        "slug",
        "start_at",
        "end_at",
        "is_published",
        "created_at",
    )
    search_fields = ("name", "slug", "description")
    list_filter = ("is_published", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("start_at",)
