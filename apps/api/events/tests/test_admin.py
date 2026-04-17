import pytest
from django.contrib import admin

from events.models import Event


@pytest.mark.django_db
def test_event_is_registered_in_admin() -> None:
    assert Event in admin.site._registry


@pytest.mark.django_db
def test_event_admin_configuration() -> None:
    event_admin = admin.site._registry[Event]

    assert "name" in event_admin.list_display
    assert "slug" in event_admin.list_display
    assert "is_published" in event_admin.list_display
    assert "name" in event_admin.search_fields
    assert "is_published" in event_admin.list_filter
    assert event_admin.prepopulated_fields == {"slug": ("name",)}
