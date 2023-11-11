from typing import ClassVar, Self

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from digitaldome.common.models import TimestampedModel


class TrackingObject(TimestampedModel):
    class Status(models.IntegerChoices):
        PLANNED = 0, "Planned"
        IN_PROGRESS = 1, "In Progress"
        COMPLETED = 2, "Completed"
        DROPPED = 3, "Dropped"
        ON_HOLD = 4, "On Hold"

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey("content_type", "object_id")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.COMPLETED, blank=True)

    rating = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    notes = models.TextField(blank=True, validators=[MaxLengthValidator(150)])

    class Meta:
        indexes: ClassVar = [
            models.Index(fields=["object_id", "content_type"]),
            models.Index(fields=["user", "status"]),
        ]
        constraints: ClassVar = [
            models.UniqueConstraint(fields=["object_id", "content_type", "user"], name="unique_tracking_object"),
        ]


class UserStats(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # All time spent is in seconds.
    time_spent_on_movies = models.BigIntegerField(default=0)

    class Meta:
        verbose_name_plural = _("User Stats")
        verbose_name = _("User Stats")

    def __str__(self: Self) -> str:
        return f"{self.user.display_name} (stats)"
