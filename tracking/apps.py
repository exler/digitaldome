from typing import Self

from django.apps import AppConfig


class TrackingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tracking"

    def ready(self: Self) -> None:
        # Make sure the receivers are imported
        from tracking import receivers  # noqa: F401
