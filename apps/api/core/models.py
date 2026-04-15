import uuid

from django.db import models


class UUIDModel(models.Model):
    """
    An abstract base class model that makes the primary key a UUID instead of
    an auto-incrementing integer.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this instance.",
    )

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="The date and time this record was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_index=True,
        help_text="The date and time this record was last updated.",
    )

    class Meta:
        abstract = True
        # By default, order by creation date descending
        ordering = ["-created_at"]


class BaseDomainModel(UUIDModel, TimeStampedModel):
    """
    A convenience abstract base class combining UUID primary keys
    and timestamped fields for standard domain models.
    """

    class Meta:
        abstract = True
