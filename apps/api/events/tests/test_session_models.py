import uuid

import pytest
from django.db import IntegrityError
from django.db.models import Manager
from django.utils import timezone

from events.models import Session


def get_session_manager() -> Manager[Session]:
    return Session._default_manager


@pytest.mark.django_db
def test_session_can_be_created() -> None:
    session = get_session_manager().create(
        title="Opening Keynote",
        slug="opening-keynote",
        description="Welcome and keynote session.",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )

    assert session.title == "Opening Keynote"
    assert session.slug == "opening-keynote"
    assert session.is_published is False


@pytest.mark.django_db
def test_session_id_is_uuid() -> None:
    session = get_session_manager().create(
        title="UUID Session",
        slug="uuid-session",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )

    assert isinstance(session.id, uuid.UUID)


@pytest.mark.django_db
def test_session_has_timestamps() -> None:
    session = get_session_manager().create(
        title="Timed Session",
        slug="timed-session",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )

    assert session.created_at is not None
    assert session.updated_at is not None


@pytest.mark.django_db
def test_session_slug_must_be_unique() -> None:
    get_session_manager().create(
        title="First Session",
        slug="same-slug",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )

    with pytest.raises(IntegrityError):
        get_session_manager().create(
            title="Second Session",
            slug="same-slug",
            start_at=timezone.now(),
            end_at=timezone.now(),
        )


@pytest.mark.django_db
def test_session_string_representation_returns_title() -> None:
    session = get_session_manager().create(
        title="Closing Remarks",
        slug="closing-remarks",
        start_at=timezone.now(),
        end_at=timezone.now(),
    )

    assert str(session) == "Closing Remarks"
