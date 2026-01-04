import argparse
from typing import Any, Optional

from django.apps import apps
from django.conf import settings
from django.core.files.storage import Storage, storages
from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):
    help = "Delete files from storage backends that are no longer used by any model instance."

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--storage",
            type=str,
            default="default",
            help="Specify the storage backend to clean up files from.",
        )
        parser.add_argument(
            "--dry-run", action="store_true", help="List files that would be deleted without actually deleting them."
        )

    def handle(self, *args: Any, **options: Any) -> None:
        target_storage_key = options["storage"]

        self.stdout.write(f"Loading target storage {target_storage_key}...")
        target_storage = self._get_storage(target_storage_key)

        if target_storage is None:
            self.stderr.write(self.style.ERROR("Error loading storage. Check STORAGES settings."))
            return

        self.stdout.write("Collecting used file paths from models...")
        self.used_file_paths = set()

        for django_app in apps.get_models():
            file_fields = [
                field
                for field in django_app._meta.get_fields()
                if isinstance(field, (models.FileField, models.ImageField))
            ]

            for instance in django_app.objects.only(*[field.name for field in file_fields]).iterator():
                for field in file_fields:
                    file_field = getattr(instance, field.name)
                    if file_field and file_field.storage == target_storage:
                        self.used_file_paths.add(file_field.name)

        self.stdout.write(self.style.SUCCESS(f"Found {len(self.used_file_paths)} used file paths."))
        self.stdout.write("Scanning storage for unused files...")

        self._delete_files_in_directory(target_storage, "", options["dry_run"])

        self.stdout.write(self.style.SUCCESS("Cleanup complete."))

    def _get_storage(self, key: str) -> Optional[Storage]:
        """
        Instantiate a storage backend from settings.STORAGES[key].
        """

        if key not in settings.STORAGES:
            self.stderr.write(f"Storage '{key}' not found in settings.STORAGES.")
            return None

        return storages[key]

    def _delete_files_in_directory(self, storage: Storage, directory: str, dry_run: bool) -> None:
        """
        Recursively delete files in the given storage that are not in self.used_file_paths
        and call itself for subdirectories.
        """
        directories, files = storage.listdir(directory)

        for file in files:
            file_path = f"{directory}/{file}" if directory else file
            if file_path not in self.used_file_paths:
                if dry_run:
                    self.stdout.write(f"[Dry Run] Would delete: {file_path}")
                else:
                    storage.delete(file_path)
                    self.stdout.write(self.style.SUCCESS(f"Deleted: {file_path}"))

        for subdirectory in directories:
            subdirectory_path = f"{directory}/{subdirectory}" if directory else subdirectory
            self._delete_files_in_directory(storage, subdirectory_path, dry_run)
