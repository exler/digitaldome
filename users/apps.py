from typing import Self

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self: Self) -> None:
        # Make sure the receivers are imported
        from users import receivers  # noqa: F401
