from datetime import timedelta

import pytest
from django.db import IntegrityError
from django.utils import timezone

from events.models import Event
from events.services import CreateEventService, UpdateEventService


@pytest.mark.django_db
def test_create_event_service_creates_event() -> None:
    now = timezone.now()

    event = CreateEventService(
        name="Nordic Stage 2026",
        slug="nordic-stage-2026",
        description="Flagship event",
        start_at=now,
        end_at=now + timedelta(hours=8),
    ).process()

    assert isinstance(event, Event)
    assert event.name == "Nordic Stage 2026"
    assert event.slug == "nordic-stage-2026"
    assert event.description == "Flagship event"
    assert event.is_published is False


@pytest.mark.django_db
def test_create_event_service_allows_published_event() -> None:
    now = timezone.now()

    event = CreateEventService(
        name="Published Event",
        slug="published-event",
        start_at=now,
        end_at=now + timedelta(hours=1),
        is_published=True,
    ).process()

    assert event.is_published is True


@pytest.mark.django_db
def test_create_event_service_raises_on_duplicate_slug() -> None:
    now = timezone.now()

    CreateEventService(
        name="First Event",
        slug="same-slug",
        start_at=now,
        end_at=now + timedelta(hours=1),
    ).process()

    with pytest.raises(IntegrityError):
        CreateEventService(
            name="Second Event",
            slug="same-slug",
            start_at=now,
            end_at=now + timedelta(hours=2),
        ).process()


@pytest.mark.django_db
def test_update_event_service_updates_event_fields() -> None:
    now = timezone.now()
    event = Event.objects.create(
        name="Original Event",
        slug="original-event",
        description="Original description",
        start_at=now,
        end_at=now + timedelta(hours=1),
        is_published=False,
    )

    updated_event = UpdateEventService(
        event=event,
        name="Updated Event",
        slug="updated-event",
        description="Updated description",
        start_at=now + timedelta(days=1),
        end_at=now + timedelta(days=1, hours=2),
        is_published=True,
    ).process()

    assert updated_event.id == event.id
    assert updated_event.name == "Updated Event"
    assert updated_event.slug == "updated-event"
    assert updated_event.description == "Updated description"
    assert updated_event.is_published is True


@pytest.mark.django_db
def test_update_event_service_persists_changes() -> None:
    now = timezone.now()
    event = Event.objects.create(
        name="Persisted Event",
        slug="persisted-event",
        start_at=now,
        end_at=now + timedelta(hours=1),
    )

    UpdateEventService(
        event=event,
        name="Persisted Event Updated",
        slug="persisted-event-updated",
        description="Now updated",
        start_at=now + timedelta(days=2),
        end_at=now + timedelta(days=2, hours=1),
        is_published=True,
    ).process()

    event.refresh_from_db()

    assert event.name == "Persisted Event Updated"
    assert event.slug == "persisted-event-updated"
    assert event.description == "Now updated"
    assert event.is_published is True
