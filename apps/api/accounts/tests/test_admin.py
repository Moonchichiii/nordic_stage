import pytest
from django.contrib import admin

from accounts.models import Profile, User


@pytest.mark.django_db
def test_user_is_registered_in_admin() -> None:
    assert User in admin.site._registry


@pytest.mark.django_db
def test_profile_is_registered_in_admin() -> None:
    assert Profile in admin.site._registry


@pytest.mark.django_db
def test_user_admin_configuration() -> None:
    user_admin = admin.site._registry[User]

    assert "email" in user_admin.list_display
    assert "email" in user_admin.search_fields


@pytest.mark.django_db
def test_profile_admin_configuration() -> None:
    profile_admin = admin.site._registry[Profile]

    assert "display_name" in profile_admin.list_display
    assert "user__email" in profile_admin.search_fields
