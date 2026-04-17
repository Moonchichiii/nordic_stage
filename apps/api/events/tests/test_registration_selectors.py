from uuid import UUID

import pytest
from django.utils import timezone

from events.models import Event, Registration, RegistrationStatus
from events.selectors import (
    get_all_registrations,
    get_confirmed_registrations,
    get_registration_by_email,
    get_registration_by_id,
    get_registrations_for_event,
)


def create_event(name: str, slug: str) -> Event:
    now = timezone.now()
    return Event.objects.create(
        name=name,
        slug=slug,
        start_at=now,
        end_at=now,
    )


def create_registration(event: Event, email: str) -> Registration:
    return Registration.objects.create(
        event=event,
        email=email,
        full_name="Test User",
    )


@pytest.mark.django_db
def test_get_all_registrations_returns_all() -> None:
    event = create_event("Event A", "event-a")

    create_registration(event, "a@example.com")
    create_registration(event, "b@example.com")

    result = get_all_registrations()

    assert len(result) == 2


@pytest.mark.django_db
def test_get_registrations_for_event_returns_only_event() -> None:
    event1 = create_event("Event A", "event-a")
    event2 = create_event("Event B", "event-b")

    create_registration(event1, "a@example.com")
    create_registration(event2, "b@example.com")

    result = get_registrations_for_event(event_id=event1.id)

    assert len(result) == 1
    assert result[0].event == event1


@pytest.mark.django_db
def test_get_registration_by_id_returns_correct_registration() -> None:
    event = create_event("Event A", "event-a")
    registration = create_registration(event, "a@example.com")

    result = get_registration_by_id(registration_id=registration.id)

    assert result is not None
    assert result.id == registration.id


@pytest.mark.django_db
def test_get_registration_by_id_returns_none_if_missing() -> None:
    result = get_registration_by_id(
        registration_id=UUID("00000000-0000-0000-0000-000000000000")
    )

    assert result is None


@pytest.mark.django_db
def test_get_registration_by_email_returns_correct_registration() -> None:
    event = create_event("Event A", "event-a")
    create_registration(event, "a@example.com")

    result = get_registration_by_email(
        event_id=event.id,
        email="a@example.com",
    )

    assert result is not None
    assert result.email == "a@example.com"


@pytest.mark.django_db
def test_get_confirmed_registrations_returns_only_confirmed() -> None:
    event = create_event("Event A", "event-a")

    confirmed = create_registration(event, "confirmed@example.com")
    confirmed.status = RegistrationStatus.CONFIRMED
    confirmed.save()

    create_registration(event, "pending@example.com")

    result = get_confirmed_registrations(event_id=event.id)

    assert len(result) == 1
    assert result[0].email == "confirmed@example.com"
