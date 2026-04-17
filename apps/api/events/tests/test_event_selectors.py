from datetime import timedelta

import pytest
from django.utils import timezone

from events.models import Event
from events.selectors import (
    get_all_events,
    get_event_by_slug,
    get_past_events,
    get_published_events,
    get_upcoming_events,
)


@pytest.mark.django_db
def test_get_all_events_returns_all_events() -> None:
    Event.objects.create(
        name="Event 1",
        slug="event-1",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )
    Event.objects.create(
        name="Event 2",
        slug="event-2",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )

    events = get_all_events()

    assert events.count() == 2


@pytest.mark.django_db
def test_get_published_events_returns_only_published() -> None:
    Event.objects.create(
        name="Published",
        slug="published",
        start_at=timezone.now(),
        end_at=timezone.now(),
        is_published=True,
    )
    Event.objects.create(
        name="Draft",
        slug="draft",
        start_at=timezone.now(),
        end_at=timezone.now(),
        is_published=False,
    )

    events = get_published_events()

    assert events.count() == 1
    event = events.first()
    assert event is not None
    assert event.slug == "published"


@pytest.mark.django_db
def test_get_upcoming_events_returns_future_events() -> None:
    now = timezone.now()

    Event.objects.create(
        name="Future",
        slug="future",
        start_at=now + timedelta(days=1),
        end_at=now + timedelta(days=1, hours=1),
    )
    Event.objects.create(
        name="Past",
        slug="past",
        start_at=now - timedelta(days=2),
        end_at=now - timedelta(days=1),
    )

    events = get_upcoming_events()

    assert events.count() == 1
    event = events.first()
    assert event is not None
    assert event.slug == "future"


@pytest.mark.django_db
def test_get_past_events_returns_finished_events() -> None:
    now = timezone.now()

    Event.objects.create(
        name="Past",
        slug="past",
        start_at=now - timedelta(days=2),
        end_at=now - timedelta(days=1),
    )
    Event.objects.create(
        name="Future",
        slug="future",
        start_at=now + timedelta(days=1),
        end_at=now + timedelta(days=2),
    )

    events = get_past_events()

    assert events.count() == 1
    event = events.first()
    assert event is not None
    assert event.slug == "past"


@pytest.mark.django_db
def test_get_event_by_slug_returns_correct_event() -> None:
    event = Event.objects.create(
        name="Target",
        slug="target-event",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )

    result = get_event_by_slug("target-event")

    assert result is not None
    assert result.id == event.id
