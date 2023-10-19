from typing import Any, Iterable

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from entities.models import Movie
from tracking.models import TrackingObject, UserStats


@receiver(pre_save, sender=TrackingObject)
def update_user_stats_pre_save(
    sender: type[TrackingObject], instance: TrackingObject, update_fields: Iterable[str], **kwargs: Any
) -> None:
    if update_fields and "status" not in update_fields:
        return

    created = instance._state.adding
    if created and instance.status != TrackingObject.Status.COMPLETED:
        return

    if not created:
        old_instance = TrackingObject.objects.get(pk=instance.pk)
        has_status_changed = old_instance.status != instance.status
        if not has_status_changed:
            return

        if (
            instance.status != TrackingObject.Status.COMPLETED
            and old_instance.status != TrackingObject.Status.COMPLETED
        ):
            return

    user_stats = UserStats.objects.get_or_create(user=instance.user)[0]
    if instance.content_type == ContentType.objects.get_for_model(Movie):
        if instance.status == TrackingObject.Status.COMPLETED:
            user_stats.time_spent_on_movies += instance.content_object.length
        else:
            user_stats.time_spent_on_movies -= instance.content_object.length

        user_stats.save(update_fields=["time_spent_on_movies"])


@receiver(post_delete, sender=TrackingObject)
def update_user_stats_post_delete(sender: type[TrackingObject], instance: TrackingObject, **kwargs: Any) -> None:
    if instance.status != TrackingObject.Status.COMPLETED:
        return

    user_stats = UserStats.objects.get(user=instance.user)
    if instance.content_type == ContentType.objects.get_for_model(Movie):
        user_stats.time_spent_on_movies -= instance.content_object.length
        user_stats.save(update_fields=["time_spent_on_movies"])
