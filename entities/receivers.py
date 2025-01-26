from typing import Any

from django.db.models.signals import post_delete
from django.db.transaction import on_commit
from django.dispatch import receiver

from entities.models import Book, EntityBase, Game, Movie, Show


@receiver(post_delete, sender=Movie)
@receiver(post_delete, sender=Show)
@receiver(post_delete, sender=Game)
@receiver(post_delete, sender=Book)
def delete_tracking_objects_on_parent_deletion(instance: EntityBase, **kwargs: Any) -> None:
    """Delete the image file in storage when the parent object is deleted."""

    on_commit(lambda: instance.image.delete(save=False))
