import uuid
from typing import cast

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from accounts.models import User


def get_user_model_class() -> type[User]:
    return cast(type[User], get_user_model())


@pytest.mark.django_db
def test_auth_user_model_setting() -> None:
    assert settings.AUTH_USER_MODEL == "accounts.User"


@pytest.mark.django_db
def test_user_can_be_created() -> None:
    user_model = get_user_model_class()
    user = user_model.objects.create_user(
        username="moon",
        email="moon@example.com",
        password="super-secret-123",
    )

    assert user.username == "moon"
    assert user.email == "moon@example.com"
    assert user.check_password("super-secret-123") is True


@pytest.mark.django_db
def test_user_id_is_uuid() -> None:
    user_model = get_user_model_class()
    user = user_model.objects.create_user(
        username="uuiduser",
        email="uuid@example.com",
        password="super-secret-123",
    )

    assert isinstance(user.id, uuid.UUID)


@pytest.mark.django_db
def test_user_has_timestamps() -> None:
    user_model = get_user_model_class()
    user = user_model.objects.create_user(
        username="timeduser",
        email="timed@example.com",
        password="super-secret-123",
    )

    assert user.created_at is not None
    assert user.updated_at is not None


@pytest.mark.django_db
def test_email_must_be_unique() -> None:
    user_model = get_user_model_class()
    user_model.objects.create_user(
        username="firstuser",
        email="same@example.com",
        password="super-secret-123",
    )

    with pytest.raises(IntegrityError):
        user_model.objects.create_user(
            username="seconduser",
            email="same@example.com",
            password="super-secret-456",
        )


@pytest.mark.django_db
def test_string_representation_returns_username() -> None:
    user_model = get_user_model_class()
    user = user_model.objects.create_user(
        username="displayname",
        email="display@example.com",
        password="super-secret-123",
    )

    assert str(user) == "displayname"
