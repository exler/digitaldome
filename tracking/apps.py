from typing import Self

from django.apps import AppConfig


class TrackingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tracking"

    def ready(self: Self) -> None:
        import tracking.receivers  # noqa: F401
