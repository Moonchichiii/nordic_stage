import uuid

import pytest
from django.db import IntegrityError
from django.db.models import Manager

from events.models import Speaker


def get_speaker_manager() -> Manager[Speaker]:
    return Speaker._default_manager


@pytest.mark.django_db
def test_speaker_can_be_created() -> None:
    speaker = get_speaker_manager().create(
        full_name="Ada Lovelace",
        slug="ada-lovelace",
        bio="Pioneer in computing.",
        job_title="Mathematician",
        company_name="Analytical Engine",
    )

    assert speaker.full_name == "Ada Lovelace"
    assert speaker.slug == "ada-lovelace"
    assert speaker.is_published is False


@pytest.mark.django_db
def test_speaker_id_is_uuid() -> None:
    speaker = get_speaker_manager().create(
        full_name="UUID Speaker",
        slug="uuid-speaker",
    )

    assert isinstance(speaker.id, uuid.UUID)


@pytest.mark.django_db
def test_speaker_has_timestamps() -> None:
    speaker = get_speaker_manager().create(
        full_name="Timed Speaker",
        slug="timed-speaker",
    )

    assert speaker.created_at is not None
    assert speaker.updated_at is not None


@pytest.mark.django_db
def test_speaker_slug_must_be_unique() -> None:
    get_speaker_manager().create(
        full_name="First Speaker",
        slug="same-slug",
    )

    with pytest.raises(IntegrityError):
        get_speaker_manager().create(
            full_name="Second Speaker",
            slug="same-slug",
        )


@pytest.mark.django_db
def test_speaker_string_representation_returns_full_name() -> None:
    speaker = get_speaker_manager().create(
        full_name="Grace Hopper",
        slug="grace-hopper",
    )

    assert str(speaker) == "Grace Hopper"
