import uuid

import pytest
from django.db import IntegrityError
from django.db.models import Manager
from django.utils import timezone

from events.models import Event


def get_event_manager() -> Manager[Event]:
    return Event._default_manager


@pytest.mark.django_db
def test_event_can_be_created() -> None:
    event = get_event_manager().create(
        name="Nordic Stage 2026",
        slug="nordic-stage-2026",
        description="A flagship event",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )

    assert event.name == "Nordic Stage 2026"
    assert event.slug == "nordic-stage-2026"
    assert event.is_published is False


@pytest.mark.django_db
def test_event_id_is_uuid() -> None:
    event = get_event_manager().create(
        name="UUID Event",
        slug="uuid-event",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )

    assert isinstance(event.id, uuid.UUID)


@pytest.mark.django_db
def test_event_has_timestamps() -> None:
    event = get_event_manager().create(
        name="Timed Event",
        slug="timed-event",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )

    assert event.created_at is not None
    assert event.updated_at is not None


@pytest.mark.django_db
def test_event_slug_must_be_unique() -> None:
    get_event_manager().create(
        name="First Event",
        slug="same-slug",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )

    with pytest.raises(IntegrityError):
        get_event_manager().create(
            name="Second Event",
            slug="same-slug",
            start_at=timezone.now(),
            end_at=timezone.now(),
        )


@pytest.mark.django_db
def test_event_string_representation_returns_name() -> None:
    event = get_event_manager().create(
        name="String Event",
        slug="string-event",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )

    assert str(event) == "String Event"
