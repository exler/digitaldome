import subprocess  # nosec
import sys
from typing import Any, Self

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Removes the Postgres database and its volume and creates a fresh one."

    def handle(self: Self, *args: Any, **options: Any) -> None:
        # Prompt the user for confirmation
        if input("Are you sure you want to reset the database? [y/N] ").lower() != "y":
            self.stdout.write("Aborted.")
            return

        self.stdout.write(self.style.WARNING("Resetting the database..."))

        subprocess.run(
            ["docker-compose", "down", "-v", "db"],
            stdout=subprocess.DEVNULL,
            stderr=sys.stderr,
        )  # nosec
        subprocess.run(
            ["docker-compose", "up", "-d", "db"],
            stdout=subprocess.DEVNULL,
            stderr=sys.stderr,
        )  # nosec

        self.stdout.write(self.style.SUCCESS("Done."))
