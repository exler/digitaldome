from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete
from django.db.transaction import on_commit
from django.dispatch import receiver

from entities.models import Book, EntityBase, Game, Movie, Show
from tracking.models import TrackingObject


@receiver(post_delete, sender=Movie)
@receiver(post_delete, sender=Show)
@receiver(post_delete, sender=Game)
@receiver(post_delete, sender=Book)
def delete_tracking_objects_on_parent_deletion(sender: type[EntityBase], instance: EntityBase, **kwargs: Any) -> None:
    """Delete all TrackingObjects related to the parent object when it's deleted."""

    content_type = ContentType.objects.get_for_model(sender)
    on_commit(lambda: TrackingObject.objects.filter(object_id=instance.id, content_type=content_type).delete())
