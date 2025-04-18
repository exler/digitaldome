# yourapp/management/commands/migrate_storage.py

import argparse
from typing import Any, Optional

from django.conf import settings
from django.core.files.storage import Storage, storages
from django.core.management.base import BaseCommand
from django.db.models import Model

from entities.models import Book, Game, Movie, Show
from users.models import User


class Command(BaseCommand):
    help = "Migrate files the currently used storage backend to another"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--target", type=str, default="new", help="STORAGES key name for target storage (default: 'new')"
        )

    def handle(self, *args: Any, **options: Any) -> None:
        target_key = options["target"]

        self.stdout.write(f"Loading target storage '{target_key}'...")
        target_storage = self.get_storage(target_key)

        if target_storage is None:
            self.stderr.write("Error loading storage. Check STORAGES settings.")
            return

        self.stdout.write(f"Starting migration from to storage '{target_key}'...")
        self.migrate_entities(target_storage)
        self.migrate_users(target_storage)
        self.stdout.write(self.style.SUCCESS("Migration finished"))

    def get_storage(self, key: str) -> Optional[Storage]:
        """
        Instantiate a storage backend from settings.STORAGES[key].
        """

        if key not in settings.STORAGES:
            self.stderr.write(f"Storage '{key}' not found in settings.STORAGES.")
            return None

        return storages[key]

    def migrate_entities(self, target: Storage) -> None:
        """
        Copy all files related to database entities to the target storage.
        """

        for entity in [Game, Show, Movie, Book]:
            self.stdout.write(f"Migrating {entity.__name__}...")
            for obj in entity.objects.iterator():
                self.migrate_object(obj, "image", target)

    def migrate_users(self, target: Storage) -> None:
        """
        Copy all files related to users to the target storage.
        """

        self.stdout.write("Migrating users...")
        for obj in User.objects.iterator():
            self.migrate_object(obj, "avatar", target)

    def migrate_object(self, obj: Model, field_name: str, target: Storage) -> None:
        if not (field := getattr(obj, field_name, None)):
            self.stderr.write(f"Field '{field_name}' does not exist on {obj}.")
            return

        if field.storage == target:
            self.stdout.write(f"Field '{field_name}' already uses the target storage.")
            return

        if not target.exists(field.name):
            self.stdout.write(f"Copying file for {obj}...")
            target.save(field.name, field.file)
            self.stdout.write(self.style.SUCCESS(f"File for {obj} copied."))
        else:
            self.stdout.write(f"File for {obj} already exists in target storage. Skipping...")
            return
