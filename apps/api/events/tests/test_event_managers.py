from datetime import timedelta

import pytest
from django.utils import timezone

from events.models import Event


@pytest.mark.django_db
def test_event_manager_published_returns_only_published_events() -> None:
    now = timezone.now()

    published_event = Event.objects.create(
        name="Published Event",
        slug="published-event",
        start_at=now,
        end_at=now + timedelta(hours=1),
        is_published=True,
    )
    Event.objects.create(
        name="Draft Event",
        slug="draft-event",
        start_at=now,
        end_at=now + timedelta(hours=1),
        is_published=False,
    )

    events = Event.objects.published()

    assert list(events) == [published_event]


@pytest.mark.django_db
def test_event_manager_upcoming_returns_only_future_events() -> None:
    now = timezone.now()

    upcoming_event = Event.objects.create(
        name="Upcoming Event",
        slug="upcoming-event",
        start_at=now + timedelta(days=1),
        end_at=now + timedelta(days=1, hours=1),
    )
    Event.objects.create(
        name="Past Event",
        slug="past-event",
        start_at=now - timedelta(days=2),
        end_at=now - timedelta(days=2, hours=-1),
    )

    events = Event.objects.upcoming()

    assert list(events) == [upcoming_event]


@pytest.mark.django_db
def test_event_manager_past_returns_only_finished_events() -> None:
    now = timezone.now()

    past_event = Event.objects.create(
        name="Past Event",
        slug="past-event-2",
        start_at=now - timedelta(days=2),
        end_at=now - timedelta(days=1),
    )
    Event.objects.create(
        name="Upcoming Event",
        slug="upcoming-event-2",
        start_at=now + timedelta(days=1),
        end_at=now + timedelta(days=1, hours=1),
    )

    events = Event.objects.past()

    assert list(events) == [past_event]
