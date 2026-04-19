from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from django.utils import timezone

from events.models import (
    Event,
    Order,
    PaymentEvent,
    PaymentEventType,
    Registration,
)
from events.services import CreateStripeCheckoutSessionService


def create_order() -> Order:
    now = timezone.now()
    event = Event.objects.create(
        name="Nordic Stage 2026",
        slug="nordic-stage-2026",
        start_at=now,
        end_at=now,
    )
    registration = Registration.objects.create(
        event=event,
        email="ada@example.com",
        full_name="Ada Lovelace",
    )
    return Order.objects.create(
        registration=registration,
        amount=Decimal("199.00"),
        currency="EUR",
    )


@pytest.mark.django_db
def test_create_stripe_checkout_session_service_calls_gateway() -> None:
    order = create_order()
    gateway = MagicMock()
    gateway.create_checkout_session.return_value = SimpleNamespace(
        id="cs_test_123"
    )

    session = CreateStripeCheckoutSessionService(
        order=order,
        gateway=gateway,
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    ).process()

    assert session.id == "cs_test_123"
    gateway.create_checkout_session.assert_called_once_with(
        amount=19900,
        currency="eur",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        metadata={"order_id": str(order.id)},
    )


@pytest.mark.django_db
def test_create_stripe_checkout_session_service_logs_payment_event() -> None:
    order = create_order()
    gateway = MagicMock()
    gateway.create_checkout_session.return_value = SimpleNamespace(
        id="cs_test_456"
    )

    CreateStripeCheckoutSessionService(
        order=order,
        gateway=gateway,
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    ).process()

    payment_event = PaymentEvent.objects.get(order=order)

    assert payment_event.event_type == PaymentEventType.CREATED
    assert payment_event.provider == "stripe"
    assert payment_event.provider_event_id == "cs_test_456"
    assert payment_event.payload == {"checkout_session_id": "cs_test_456"}
