from typing import Any

from django.db.models.signals import post_delete
from django.db.transaction import on_commit
from django.dispatch import receiver

from users.models import User


@receiver(post_delete, sender=User)
def delete_tracking_objects_on_parent_deletion(instance: User, **kwargs: Any) -> None:
    """Delete the image file in storage when the parent object is deleted."""

    on_commit(lambda: instance.avatar.delete(save=False))
