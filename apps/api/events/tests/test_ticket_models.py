import uuid

import pytest
from django.db import IntegrityError
from django.db.models import Manager
from django.utils import timezone

from events.models import (
    Event,
    Registration,
    Ticket,
    TicketStatus,
)


def get_ticket_manager() -> Manager[Ticket]:
    return Ticket._default_manager


def create_event() -> Event:
    now = timezone.now()
    return Event.objects.create(
        name="Nordic Stage 2026",
        slug="nordic-stage-2026",
        start_at=now,
        end_at=now,
    )


def create_registration() -> Registration:
    event = create_event()
    return Registration.objects.create(
        event=event,
        email="ada@example.com",
        full_name="Ada Lovelace",
    )


@pytest.mark.django_db
def test_ticket_can_be_created() -> None:
    registration = create_registration()

    ticket = get_ticket_manager().create(
        registration=registration,
        code="TICKET-001",
    )

    assert ticket.registration == registration
    assert ticket.code == "TICKET-001"
    assert ticket.status == TicketStatus.ACTIVE


@pytest.mark.django_db
def test_ticket_id_is_uuid() -> None:
    registration = create_registration()

    ticket = get_ticket_manager().create(
        registration=registration,
        code="UUID-TICKET",
    )

    assert isinstance(ticket.id, uuid.UUID)


@pytest.mark.django_db
def test_ticket_has_timestamps() -> None:
    registration = create_registration()

    ticket = get_ticket_manager().create(
        registration=registration,
        code="TIMED-TICKET",
    )

    assert ticket.created_at is not None
    assert ticket.updated_at is not None


@pytest.mark.django_db
def test_ticket_string_representation_returns_code() -> None:
    registration = create_registration()

    ticket = get_ticket_manager().create(
        registration=registration,
        code="DISPLAY-TICKET",
    )

    assert str(ticket) == "DISPLAY-TICKET"


@pytest.mark.django_db
def test_ticket_code_must_be_unique() -> None:
    first_registration = create_registration()
    second_event = Event.objects.create(
        name="Nordic Stage 2027",
        slug="nordic-stage-2027",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )
    second_registration = Registration.objects.create(
        event=second_event,
        email="grace@example.com",
        full_name="Grace Hopper",
    )

    get_ticket_manager().create(
        registration=first_registration,
        code="SAME-CODE",
    )

    with pytest.raises(IntegrityError):
        get_ticket_manager().create(
            registration=second_registration,
            code="SAME-CODE",
        )


@pytest.mark.django_db
def test_ticket_is_unique_per_registration() -> None:
    registration = create_registration()

    get_ticket_manager().create(
        registration=registration,
        code="FIRST-TICKET",
    )

    with pytest.raises(IntegrityError):
        get_ticket_manager().create(
            registration=registration,
            code="SECOND-TICKET",
        )
