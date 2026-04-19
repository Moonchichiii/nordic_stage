import uuid
from decimal import Decimal

import pytest
from django.db.models import Manager
from django.utils import timezone

from events.models import (
    Event,
    Order,
    PaymentEvent,
    PaymentEventType,
    Registration,
)


def get_payment_event_manager() -> Manager[PaymentEvent]:
    return PaymentEvent._default_manager


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


def create_order() -> Order:
    registration = create_registration()
    return Order.objects.create(
        registration=registration,
        amount=Decimal("199.00"),
        currency="EUR",
    )


@pytest.mark.django_db
def test_payment_event_can_be_created() -> None:
    order = create_order()

    payment_event = get_payment_event_manager().create(
        order=order,
        event_type=PaymentEventType.CREATED,
        provider="stripe",
        provider_event_id="evt_123",
        payload={"id": "evt_123"},
    )

    assert payment_event.order == order
    assert payment_event.event_type == PaymentEventType.CREATED
    assert payment_event.provider == "stripe"
    assert payment_event.provider_event_id == "evt_123"


@pytest.mark.django_db
def test_payment_event_id_is_uuid() -> None:
    order = create_order()

    payment_event = get_payment_event_manager().create(
        order=order,
        event_type=PaymentEventType.SUCCEEDED,
    )

    assert isinstance(payment_event.id, uuid.UUID)


@pytest.mark.django_db
def test_payment_event_has_timestamps() -> None:
    order = create_order()

    payment_event = get_payment_event_manager().create(
        order=order,
        event_type=PaymentEventType.UPDATED,
    )

    assert payment_event.created_at is not None
    assert payment_event.updated_at is not None


@pytest.mark.django_db
def test_payment_event_string_representation_returns_order_and_type() -> None:
    order = create_order()

    payment_event = get_payment_event_manager().create(
        order=order,
        event_type=PaymentEventType.FAILED,
    )

    assert str(payment_event) == f"{order.id} - failed"


@pytest.mark.django_db
def test_payment_event_payload_defaults_to_empty_dict() -> None:
    order = create_order()

    payment_event = get_payment_event_manager().create(
        order=order,
        event_type=PaymentEventType.CREATED,
    )

    assert payment_event.payload == {}

