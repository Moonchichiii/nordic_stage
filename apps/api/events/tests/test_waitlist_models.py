import uuid

import pytest
from django.db import IntegrityError
from django.db.models import Manager
from django.utils import timezone

from events.models import Event, Waitlist, WaitlistStatus


def get_waitlist_manager() -> Manager[Waitlist]:
    return Waitlist._default_manager


def create_event() -> Event:
    now = timezone.now()
    return Event.objects.create(
        name="Nordic Stage 2026",
        slug="nordic-stage-2026",
        start_at=now,
        end_at=now,
    )


@pytest.mark.django_db
def test_waitlist_entry_can_be_created() -> None:
    event = create_event()

    entry = get_waitlist_manager().create(
        event=event,
        email="ada@example.com",
        full_name="Ada Lovelace",
    )

    assert entry.event == event
    assert entry.email == "ada@example.com"
    assert entry.status == WaitlistStatus.WAITING


@pytest.mark.django_db
def test_waitlist_id_is_uuid() -> None:
    event = create_event()

    entry = get_waitlist_manager().create(
        event=event,
        email="uuid@example.com",
        full_name="UUID User",
    )

    assert isinstance(entry.id, uuid.UUID)


@pytest.mark.django_db
def test_waitlist_has_timestamps() -> None:
    event = create_event()

    entry = get_waitlist_manager().create(
        event=event,
        email="timed@example.com",
        full_name="Timed User",
    )

    assert entry.created_at is not None
    assert entry.updated_at is not None


@pytest.mark.django_db
def test_waitlist_string_representation_returns_name_and_event() -> None:
    event = create_event()

    entry = get_waitlist_manager().create(
        event=event,
        email="grace@example.com",
        full_name="Grace Hopper",
    )

    assert str(entry) == "Grace Hopper - Nordic Stage 2026"


@pytest.mark.django_db
def test_waitlist_is_unique_per_event_and_email() -> None:
    event = create_event()

    get_waitlist_manager().create(
        event=event,
        email="same@example.com",
        full_name="First Person",
    )

    with pytest.raises(IntegrityError):
        get_waitlist_manager().create(
            event=event,
            email="same@example.com",
            full_name="Second Person",
        )


@pytest.mark.django_db
def test_waitlist_allows_same_email_for_different_events() -> None:
    first_event = create_event()
    second_event = Event.objects.create(
        name="Nordic Stage 2027",
        slug="nordic-stage-2027",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )

    get_waitlist_manager().create(
        event=first_event,
        email="same@example.com",
        full_name="First Entry",
    )

    entry = get_waitlist_manager().create(
        event=second_event,
        email="same@example.com",
        full_name="Second Entry",
    )

    assert entry.event == second_event
