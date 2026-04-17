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

class Speaker(BaseDomainModel):
    objects: ClassVar[models.Manager["Speaker"]] = models.Manager()

    full_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    bio = models.TextField(blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["full_name"]

    def __str__(self) -> str:
        return self.full_name

class Session(BaseDomainModel):
    objects: ClassVar[models.Manager["Session"]] = models.Manager()

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["start_at"]

    def __str__(self) -> str:
        return self.title

class Tag(BaseDomainModel):
    objects: ClassVar[models.Manager["Tag"]] = models.Manager()

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
