from uuid import UUID

from django.db.models import QuerySet

from events.models import Event, Registration, RegistrationStatus


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


def get_all_registrations() -> list[Registration]:
    return list(Registration.objects.all())


def get_registrations_for_event(*, event_id: UUID) -> list[Registration]:
    return list(
        Registration.objects.filter(event_id=event_id)
    )


def get_registration_by_id(*, registration_id: UUID) -> Registration | None:
    return Registration.objects.filter(id=registration_id).first()


def get_registration_by_email(
    *,
    event_id: UUID,
    email: str,
) -> Registration | None:
    return Registration.objects.filter(
        event_id=event_id,
        email=email,
    ).first()


def get_confirmed_registrations(*, event_id: UUID) -> list[Registration]:
    return list(
        Registration.objects.filter(
            event_id=event_id,
            status=RegistrationStatus.CONFIRMED,
        )
    )
