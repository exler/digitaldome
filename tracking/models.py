from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

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

    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.PLANNED)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=["object_id", "content_type"]),
            models.Index(fields=["user", "status"]),
        ]
