from collections.abc import Mapping
from typing import Any

import stripe


class StripeGateway:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        stripe.api_key = api_key

    def create_checkout_session(
        self,
        *,
        amount: int,
        currency: str,
        success_url: str,
        cancel_url: str,
        metadata: Mapping[str, str] | None = None,
    ) -> Any:
        return stripe.checkout.Session.create(
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "product_data": {
                            "name": "Nordic Stage Registration",
                        },
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }
            ],
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=dict(metadata or {}),
        )

    def retrieve_event(self, event_id: str) -> Any:
        return stripe.Event.retrieve(event_id)
