import uuid
from decimal import Decimal

import pytest
from django.db import IntegrityError
from django.db.models import Manager
from django.utils import timezone

from events.models import Event, Order, OrderStatus, Registration


def get_order_manager() -> Manager[Order]:
    return Order._default_manager


def create_event() -> Event:
    now = timezone.now()
    return Event.objects.create(
        name="Nordic Stage 2026",
        slug="nordic-stage-2026",
        start_at=now,
        end_at=now,
    )


def create_registration(email: str = "ada@example.com") -> Registration:
    event = create_event()
    return Registration.objects.create(
        event=event,
        email=email,
        full_name="Ada Lovelace",
    )


@pytest.mark.django_db
def test_order_can_be_created() -> None:
    registration = create_registration()

    order = get_order_manager().create(
        registration=registration,
        amount=Decimal("199.00"),
        currency="EUR",
    )

    assert order.registration == registration
    assert order.amount == Decimal("199.00")
    assert order.currency == "EUR"
    assert order.status == OrderStatus.PENDING


@pytest.mark.django_db
def test_order_id_is_uuid() -> None:
    registration = create_registration()

    order = get_order_manager().create(
        registration=registration,
        amount=Decimal("99.00"),
        currency="EUR",
    )

    assert isinstance(order.id, uuid.UUID)


@pytest.mark.django_db
def test_order_has_timestamps() -> None:
    registration = create_registration()

    order = get_order_manager().create(
        registration=registration,
        amount=Decimal("49.00"),
        currency="EUR",
    )

    assert order.created_at is not None
    assert order.updated_at is not None


@pytest.mark.django_db
def test_order_string_representation() -> None:
    registration = create_registration()

    order = get_order_manager().create(
        registration=registration,
        amount=Decimal("149.00"),
        currency="EUR",
    )

    assert str(order) == "Ada Lovelace - 149.00 EUR"


@pytest.mark.django_db
def test_order_is_unique_per_registration() -> None:
    registration = create_registration()

    get_order_manager().create(
        registration=registration,
        amount=Decimal("100.00"),
        currency="EUR",
    )

    with pytest.raises(IntegrityError):
        get_order_manager().create(
            registration=registration,
            amount=Decimal("200.00"),
            currency="EUR",
        )


@pytest.mark.django_db
def test_order_allows_different_orders_for_different_registrations() -> None:
    first_registration = create_registration("first@example.com")
    second_registration = Registration.objects.create(
        event=Event.objects.create(
            name="Nordic Stage 2027",
            slug="nordic-stage-2027",
            start_at=timezone.now(),
            end_at=timezone.now(),
        ),
        email="second@example.com",
        full_name="Grace Hopper",
    )

    get_order_manager().create(
        registration=first_registration,
        amount=Decimal("100.00"),
        currency="EUR",
    )
    order = get_order_manager().create(
        registration=second_registration,
        amount=Decimal("200.00"),
        currency="EUR",
    )

    assert order.registration == second_registration
