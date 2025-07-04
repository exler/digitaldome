from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

from tracking.models import TrackingObject


class Command(BaseCommand):
    """
    Use this command in case the signals have not been triggered (e.g., when deleting objects by SQL directly).
    """

    help = "Delete all TrackingObject instances where the content_object does not exist"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without actually deleting anything",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=1000,
            help="Number of objects to process in each batch (default: 1000)",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        dry_run = options["dry_run"]
        batch_size = options["batch_size"]

        self.stdout.write(self.style.WARNING("Starting cleanup of orphaned TrackingObject instances..."))

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE: No objects will be deleted"))

        total_deleted = 0
        orphaned_ids = []

        # Use iterator to process objects efficiently without loading all into memory
        for tracking_obj in TrackingObject.objects.select_related("content_type").iterator(chunk_size=batch_size):
            # Check if the content_object exists
            if tracking_obj.content_object is None:
                orphaned_ids.append(tracking_obj.id)
                self.stdout.write(
                    f"Found orphaned TrackingObject (ID: {tracking_obj.id}) - "
                    f"Content Type: {tracking_obj.content_type}, "
                    f"Object ID: {tracking_obj.object_id}"
                )

                # Delete in batches to avoid memory issues and large queries
                if len(orphaned_ids) >= batch_size:
                    if not dry_run:
                        with transaction.atomic():
                            deleted_count = TrackingObject.objects.filter(id__in=orphaned_ids).delete()[0]
                            total_deleted += deleted_count
                            self.stdout.write(
                                self.style.SUCCESS(f"Deleted {deleted_count} orphaned TrackingObject instances")
                            )
                    else:
                        total_deleted += len(orphaned_ids)
                        self.stdout.write(
                            self.style.WARNING(f"Would delete {len(orphaned_ids)} orphaned TrackingObject instances")
                        )
                    orphaned_ids = []

        # Delete any remaining orphaned objects
        if orphaned_ids:
            if not dry_run:
                with transaction.atomic():
                    deleted_count = TrackingObject.objects.filter(id__in=orphaned_ids).delete()[0]
                    total_deleted += deleted_count
                    self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} orphaned TrackingObject instances"))
            else:
                total_deleted += len(orphaned_ids)
                self.stdout.write(
                    self.style.WARNING(f"Would delete {len(orphaned_ids)} orphaned TrackingObject instances")
                )

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f"DRY RUN COMPLETE: Found {total_deleted} orphaned TrackingObject instances that would be deleted"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"CLEANUP COMPLETE: Deleted {total_deleted} orphaned TrackingObject instances")
            )
