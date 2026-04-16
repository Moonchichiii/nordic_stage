import pytest
from django.db import IntegrityError

from accounts.models import Profile, User
from accounts.services import CreateUserWithProfileService


@pytest.mark.django_db
def test_create_user_with_profile_service_creates_user() -> None:
    service = CreateUserWithProfileService(
        username="moon",
        email="moon@example.com",
        password="super-secret-123",
        display_name="Moon",
    )

    user = service.process()

    assert isinstance(user, User)
    assert user.username == "moon"
    assert user.email == "moon@example.com"
    assert user.check_password("super-secret-123") is True


@pytest.mark.django_db
def test_create_user_with_profile_service_creates_profile() -> None:
    service = CreateUserWithProfileService(
        username="profileuser",
        email="profile@example.com",
        password="super-secret-123",
        display_name="Profile User",
    )

    user = service.process()

    assert hasattr(user, "profile")
    assert user.profile.display_name == "Profile User"
    assert user.profile.user == user


@pytest.mark.django_db
def test_create_user_with_profile_service_allows_blank_display_name() -> None:
    service = CreateUserWithProfileService(
        username="blankprofile",
        email="blank@example.com",
        password="super-secret-123",
    )

    user = service.process()

    assert user.profile.display_name == ""
    assert str(user.profile) == user.username


@pytest.mark.django_db
def test_create_user_with_profile_service_raises_on_duplicate_email() -> None:
    CreateUserWithProfileService(
        username="firstuser",
        email="same@example.com",
        password="super-secret-123",
        display_name="First",
    ).process()

    with pytest.raises(IntegrityError):
        CreateUserWithProfileService(
            username="seconduser",
            email="same@example.com",
            password="super-secret-456",
            display_name="Second",
        ).process()


@pytest.mark.django_db
def test_create_user_with_profile_service_creates_one_profile_for_user() -> (
    None
):
    service = CreateUserWithProfileService(
        username="oneprofile",
        email="oneprofile@example.com",
        password="super-secret-123",
        display_name="One Profile",
    )

    user = service.process()

    assert Profile.objects.filter(user=user).count() == 1  # type: ignore[misc]
