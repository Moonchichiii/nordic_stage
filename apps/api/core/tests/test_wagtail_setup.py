import pytest
from django.urls import Resolver404, resolve


def test_wagtail_admin_login_url_resolves() -> None:
    match = resolve("/admin/login/")
    assert match is not None


def test_wagtail_documents_root_does_not_resolve() -> None:
    with pytest.raises(Resolver404):
        resolve("/documents/")
