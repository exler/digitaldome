from typing import Self

from django.apps import AppConfig


class EntitiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "entities"

    def ready(self: Self) -> None:
        # Make sure the receivers are imported
        from entities import receivers  # noqa: F401
