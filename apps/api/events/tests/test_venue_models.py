import uuid

import pytest
from django.db import IntegrityError
from django.db.models import Manager

from events.models import Venue


def get_venue_manager() -> Manager[Venue]:
    return Venue._default_manager


@pytest.mark.django_db
def test_venue_can_be_created() -> None:
    venue = get_venue_manager().create(
        name="Stockholm Waterfront",
        slug="stockholm-waterfront",
        description="Main conference venue",
        address="Nils Ericsons Plan 4",
        city="Stockholm",
        country="Sweden",
    )

    assert venue.name == "Stockholm Waterfront"
    assert venue.slug == "stockholm-waterfront"
    assert venue.is_active is True


@pytest.mark.django_db
def test_venue_id_is_uuid() -> None:
    venue = get_venue_manager().create(
        name="UUID Venue",
        slug="uuid-venue",
    )

    assert isinstance(venue.id, uuid.UUID)


@pytest.mark.django_db
def test_venue_has_timestamps() -> None:
    venue = get_venue_manager().create(
        name="Timed Venue",
        slug="timed-venue",
    )

    assert venue.created_at is not None
    assert venue.updated_at is not None


@pytest.mark.django_db
def test_venue_slug_must_be_unique() -> None:
    get_venue_manager().create(
        name="First Venue",
        slug="same-slug",
    )

    with pytest.raises(IntegrityError):
        get_venue_manager().create(
            name="Second Venue",
            slug="same-slug",
        )


@pytest.mark.django_db
def test_venue_string_representation_returns_name() -> None:
    venue = get_venue_manager().create(
        name="String Venue",
        slug="string-venue",
    )

    assert str(venue) == "String Venue"
