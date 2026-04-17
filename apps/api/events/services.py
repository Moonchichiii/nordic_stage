from datetime import datetime
from typing import Any

from core.services import BaseService
from events.models import Event, Registration


class CreateEventService(BaseService):
    def __init__(
        self,
        *,
        name: str,
        slug: str,
        start_at: datetime,
        end_at: datetime,
        description: str = "",
        is_published: bool = False,
    ) -> None:
        super().__init__()
        self.name = name
        self.slug = slug
        self.description = description
        self.start_at = start_at
        self.end_at = end_at
        self.is_published = is_published

    def execute(self) -> Event:
        return Event.objects.create(
            name=self.name,
            slug=self.slug,
            description=self.description,
            start_at=self.start_at,
            end_at=self.end_at,
            is_published=self.is_published,
        )


class UpdateEventService(BaseService):
    def __init__(
        self,
        *,
        event: Event,
        name: str,
        slug: str,
        description: str,
        start_at: datetime,
        end_at: datetime,
        is_published: bool,
    ) -> None:
        super().__init__()
        self.event = event
        self.name = name
        self.slug = slug
        self.description = description
        self.start_at = start_at
        self.end_at = end_at
        self.is_published = is_published

    def execute(self) -> Event:
        self.event.name = self.name
        self.event.slug = self.slug
        self.event.description = self.description
        self.event.start_at = self.start_at
        self.event.end_at = self.end_at
        self.event.is_published = self.is_published
        self.event.save()

        return self.event

class RegistrationService(BaseService):
    def create_registration(
        self,
        *,
        event: Event,
        email: str,
        full_name: str,
        status: str = "pending",
    ) -> Registration:
        return Registration.objects.create(
            event=event,
            email=email,
            full_name=full_name,
            status=status,
        )

    def update_registration(
        self,
        *,
        registration: Registration,
        **kwargs: Any,
    ) -> Registration:
        for field, value in kwargs.items():
            setattr(registration, field, value)

        registration.save()
        return registration
