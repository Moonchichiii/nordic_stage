from typing import ClassVar

from django.db import models

from core.models import BaseDomainModel


class Event(BaseDomainModel):
    objects = models.Manager["Event"]()

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["start_at"]

    def __str__(self) -> str:
        return self.name

class Venue(BaseDomainModel):
    objects: ClassVar[models.Manager["Venue"]] = models.Manager()

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
