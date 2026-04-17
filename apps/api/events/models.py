from typing import ClassVar, Self

from django.core.exceptions import ValidationError
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

    def clean(self) -> None:
        super().clean()
        if self.start_at and self.end_at and self.start_at > self.end_at:
            raise ValidationError(
                {"end_at": "Event end time cannot be before the start time."}
            )


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


class RegistrationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"


class Registration(BaseDomainModel):
    objects: ClassVar[models.Manager["Registration"]] = models.Manager()

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="registrations",
    )
    email = models.EmailField()
    full_name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=RegistrationStatus.choices,
        default=RegistrationStatus.PENDING,
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["event", "email"],
                name="unique_registration_per_event_email",
            )
        ]

    def __str__(self) -> str:
        return f"{self.full_name} - {self.event.name}"

class TicketStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    CANCELLED = "cancelled", "Cancelled"
    USED = "used", "Used"


class Ticket(BaseDomainModel):
    objects: ClassVar[models.Manager["Ticket"]] = models.Manager()

    registration = models.OneToOneField(
        Registration,
        on_delete=models.CASCADE,
        related_name="ticket",
    )
    code = models.CharField(max_length=64, unique=True)
    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.ACTIVE,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.code

class WaitlistStatus(models.TextChoices):
    WAITING = "waiting", "Waiting"
    NOTIFIED = "notified", "Notified"
    CANCELLED = "cancelled", "Cancelled"


class Waitlist(BaseDomainModel):
    objects: ClassVar[models.Manager["Waitlist"]] = models.Manager()

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="waitlist_entries",
    )
    email = models.EmailField()
    full_name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=WaitlistStatus.choices,
        default=WaitlistStatus.WAITING,
    )

    class Meta:
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["event", "email"],
                name="unique_waitlist_per_event_email",
            )
        ]

    def __str__(self) -> str:
        return f"{self.full_name} - {self.event.name}"


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    CANCELLED = "cancelled", "Cancelled"


class Order(BaseDomainModel):
    objects: ClassVar[models.Manager["Order"]] = models.Manager()

    registration = models.OneToOneField(
        Registration,
        on_delete=models.CASCADE,
        related_name="order",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="EUR")
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.registration.full_name} - {self.amount} {self.currency}"
