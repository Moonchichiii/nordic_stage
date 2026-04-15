from django.db import models


class IsActiveMixin(models.Model):
    """
    Provides an `is_active` boolean field.
    Useful for soft-deleting or toggling visibility.
    """

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Designates whether this record should be treated as active.",
    )

    class Meta:
        abstract = True


class TitleSlugMixin(models.Model):
    """
    Provides a title and a unique slug field.
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="A short label, generally used in URLs.",
    )

    class Meta:
        abstract = True
