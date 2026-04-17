import pytest
from django.db import IntegrityError
from django.utils import timezone

from events.models import Event, Registration
from events.services import RegistrationService


def create_event() -> Event:
    now = timezone.now()
    return Event.objects.create(
        name="Nordic Stage 2026",
        slug="nordic-stage-2026",
        start_at=now,
        end_at=now,
    )


@pytest.mark.django_db
def test_create_registration_service_creates_registration() -> None:
    service = RegistrationService()
    event = create_event()

    registration = service.create_registration(
        event=event,
        email="ada@example.com",
        full_name="Ada Lovelace",
    )

    assert registration.event == event
    assert registration.email == "ada@example.com"


@pytest.mark.django_db
def test_create_registration_service_raises_on_duplicate_email() -> None:
    service = RegistrationService()
    event = create_event()

    service.create_registration(
        event=event,
        email="same@example.com",
        full_name="First User",
    )

    with pytest.raises(IntegrityError):
        service.create_registration(
            event=event,
            email="same@example.com",
            full_name="Second User",
        )


@pytest.mark.django_db
def test_update_registration_service_updates_fields() -> None:
    service = RegistrationService()
    event = create_event()

    registration = service.create_registration(
        event=event,
        email="ada@example.com",
        full_name="Ada Lovelace",
    )

    updated = service.update_registration(
        registration=registration,
        full_name="Ada L.",
    )

    assert updated.full_name == "Ada L."


@pytest.mark.django_db
def test_update_registration_service_persists_changes() -> None:
    service = RegistrationService()
    event = create_event()

    registration = service.create_registration(
        event=event,
        email="persist@example.com",
        full_name="Persistent User",
    )

    service.update_registration(
        registration=registration,
        full_name="Updated Name",
    )

    refreshed = Registration.objects.get(id=registration.id)
    assert refreshed.full_name == "Updated Name"


@pytest.mark.django_db
def test_update_registration_does_not_create_new_instance() -> None:
    service = RegistrationService()
    event = create_event()

    registration = service.create_registration(
        event=event,
        email="sameid@example.com",
        full_name="Same ID",
    )

    updated = service.update_registration(
        registration=registration,
        full_name="Still Same ID",
    )

    assert updated.id == registration.id
