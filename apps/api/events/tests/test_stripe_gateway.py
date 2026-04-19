from types import SimpleNamespace
from unittest.mock import patch

from events.gateways import StripeGateway


def test_stripe_gateway_sets_api_key() -> None:
    gateway = StripeGateway(api_key="sk_test_123")

    assert gateway.api_key == "sk_test_123"


@patch("events.gateways.stripe.checkout.Session.create")
def test_create_checkout_session_calls_stripe(mock_create: object) -> None:
    mocked = mock_create
    assert hasattr(mocked, "return_value")
    mocked.return_value = SimpleNamespace(id="cs_test_123")

    gateway = StripeGateway(api_key="sk_test_123")

    session = gateway.create_checkout_session(
        amount=19900,
        currency="eur",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        metadata={"order_id": "123"},
    )

    assert session.id == "cs_test_123"
    mocked.assert_called_once()  # type: ignore[attr-defined]


@patch("events.gateways.stripe.Event.retrieve")
def test_retrieve_event_calls_stripe(mock_retrieve: object) -> None:
    mocked = mock_retrieve
    assert hasattr(mocked, "return_value")
    mocked.return_value = SimpleNamespace(id="evt_123")

    gateway = StripeGateway(api_key="sk_test_123")

    event = gateway.retrieve_event("evt_123")

    assert event.id == "evt_123"
    mocked.assert_called_once_with("evt_123")  # type: ignore[attr-defined]
