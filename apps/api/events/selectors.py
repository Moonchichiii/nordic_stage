from django.db.models import QuerySet

from events.models import Event


def get_all_events() -> QuerySet[Event]:
    return Event.objects.all()


def get_published_events() -> QuerySet[Event]:
    return Event.objects.published()


def get_upcoming_events() -> QuerySet[Event]:
    return Event.objects.upcoming()


def get_past_events() -> QuerySet[Event]:
    return Event.objects.past()


def get_event_by_slug(slug: str) -> Event:
    return Event.objects.get(slug=slug)
