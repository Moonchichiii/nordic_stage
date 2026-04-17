from typing import ClassVar, Self

from django.db import models
from django.db.models import functions

from core.models import BaseDomainModel


class EventQuerySet(models.QuerySet["Event"]):
    def published(self) -> Self:
        return self.filter(is_published=True)

    def upcoming(self) -> Self:
        return self.filter(start_at__gte=functions.Now())

    def past(self) -> Self:
        return self.filter(end_at__lt=functions.Now())


class EventManager(models.Manager["Event"]):
    def get_queryset(self) -> EventQuerySet:
        return EventQuerySet(self.model, using=self._db)

    def published(self) -> EventQuerySet:
        return self.get_queryset().published()

    def upcoming(self) -> EventQuerySet:
        return self.get_queryset().upcoming()

    def past(self) -> EventQuerySet:
        return self.get_queryset().past()


class Event(BaseDomainModel):
    objects: ClassVar[EventManager] = EventManager()

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
