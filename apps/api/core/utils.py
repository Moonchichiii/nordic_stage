from typing import Any

from django.http import HttpRequest
from django.utils.text import slugify


def get_client_ip(request: HttpRequest) -> str:
    """
    Extracts the correct client IP address from the request,
    accounting for reverse proxies (e.g., NGINX).
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # X-Forwarded-For can be a comma-separated list of IPs.
        # The first one is the original client IP.
        return str(x_forwarded_for).split(",")[0].strip()
    return str(request.META.get("REMOTE_ADDR", ""))


def generate_unique_slug(
    model_class: Any, title: str, lookup_field: str = "slug"
) -> str:
    """
    Generates a unique slug for a given Django model class.
    Appends a counter (-1, -2) if the slug already exists.
    """
    base_slug = slugify(title)
    slug = base_slug
    counter = 1

    # Loop until we find a slug that does not exist in the database
    while model_class.objects.filter(**{lookup_field: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug
