from datetime import datetime

from core.services import BaseService
from events.models import Event


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
