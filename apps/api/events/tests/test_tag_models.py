import uuid

import pytest
from django.db import IntegrityError
from django.db.models import Manager

from events.models import Tag


def get_tag_manager() -> Manager[Tag]:
    return Tag._default_manager


@pytest.mark.django_db
def test_tag_can_be_created() -> None:
    tag = get_tag_manager().create(
        name="AI",
        slug="ai",
        description="Artificial intelligence content",
    )

    assert tag.name == "AI"
    assert tag.slug == "ai"
    assert tag.is_active is True


@pytest.mark.django_db
def test_tag_id_is_uuid() -> None:
    tag = get_tag_manager().create(
        name="UUID Tag",
        slug="uuid-tag",
    )

    assert isinstance(tag.id, uuid.UUID)


@pytest.mark.django_db
def test_tag_has_timestamps() -> None:
    tag = get_tag_manager().create(
        name="Timed Tag",
        slug="timed-tag",
    )

    assert tag.created_at is not None
    assert tag.updated_at is not None


@pytest.mark.django_db
def test_tag_slug_must_be_unique() -> None:
    get_tag_manager().create(
        name="First Tag",
        slug="same-slug",
    )

    with pytest.raises(IntegrityError):
        get_tag_manager().create(
            name="Second Tag",
            slug="same-slug",
        )


@pytest.mark.django_db
def test_tag_string_representation_returns_name() -> None:
    tag = get_tag_manager().create(
        name="Python",
        slug="python",
    )

    assert str(tag) == "Python"
