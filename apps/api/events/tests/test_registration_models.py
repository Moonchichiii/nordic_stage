import uuid

import pytest
from django.db import IntegrityError
from django.db.models import Manager
from django.utils import timezone

from events.models import Event, Registration, RegistrationStatus


def get_registration_manager() -> Manager[Registration]:
    return Registration._default_manager


def create_event() -> Event:
    now = timezone.now()
    return Event.objects.create(
        name="Nordic Stage 2026",
        slug="nordic-stage-2026",
        start_at=now,
        end_at=now,
    )


@pytest.mark.django_db
def test_registration_can_be_created() -> None:
    event = create_event()

    registration = get_registration_manager().create(
        event=event,
        email="ada@example.com",
        full_name="Ada Lovelace",
    )

    assert registration.event == event
    assert registration.email == "ada@example.com"
    assert registration.full_name == "Ada Lovelace"
    assert registration.status == RegistrationStatus.PENDING


@pytest.mark.django_db
def test_registration_id_is_uuid() -> None:
    event = create_event()

    registration = get_registration_manager().create(
        event=event,
        email="uuid@example.com",
        full_name="UUID User",
    )

    assert isinstance(registration.id, uuid.UUID)


@pytest.mark.django_db
def test_registration_has_timestamps() -> None:
    event = create_event()

    registration = get_registration_manager().create(
        event=event,
        email="timed@example.com",
        full_name="Timed User",
    )

    assert registration.created_at is not None
    assert registration.updated_at is not None


@pytest.mark.django_db
def test_registration_string_representation_returns_name_and_event() -> None:
    event = create_event()

    registration = get_registration_manager().create(
        event=event,
        email="grace@example.com",
        full_name="Grace Hopper",
    )

    assert str(registration) == "Grace Hopper - Nordic Stage 2026"


@pytest.mark.django_db
def test_registration_is_unique_per_event_and_email() -> None:
    event = create_event()

    get_registration_manager().create(
        event=event,
        email="same@example.com",
        full_name="First Person",
    )

    with pytest.raises(IntegrityError):
        get_registration_manager().create(
            event=event,
            email="same@example.com",
            full_name="Second Person",
        )


@pytest.mark.django_db
def test_registration_allows_same_email_for_different_events() -> None:
    first_event = create_event()
    second_event = Event.objects.create(
        name="Nordic Stage 2027",
        slug="nordic-stage-2027",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )

    get_registration_manager().create(
        event=first_event,
        email="same@example.com",
        full_name="First Registration",
    )
    registration = get_registration_manager().create(
        event=second_event,
        email="same@example.com",
        full_name="Second Registration",
    )

    assert registration.event == second_event
