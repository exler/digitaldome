import csv
import logging
from abc import ABC, abstractmethod
from itertools import tee
from typing import ClassVar, Self

import magic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.files import File

from entities.models import Book, Movie, Show
from tracking.models import TrackingObject
from users.models import User

logger = logging.getLogger(__name__)


class BaseImporter(ABC):
    IMPORTER_NAME: str

    ALLOWED_MIME_TYPES: tuple[str, ...]

    def __init__(self: Self, user: User, source_file: File) -> None:
        self.user = user
        self.source_file = source_file

    def run(self: Self) -> None:
        self.validate()
        self.import_data()

    @abstractmethod
    def validate(self: Self) -> None: ...

    @abstractmethod
    def import_data(self: Self) -> None: ...


class CSVImporter(BaseImporter):
    ALLOWED_MIME_TYPES = ("text/csv", "text/plain")

    def validate(self: Self) -> None:
        detected_mime_type = magic.from_buffer(self.source_file.read(), mime=True)
        if detected_mime_type not in self.ALLOWED_MIME_TYPES:
            raise ValidationError("Invalid file type.")

        self.source_file.seek(0)


class GoodreadsImporter(CSVImporter):
    IMPORTER_NAME = "goodreads_csv"

    STATUS_MAPPING: ClassVar = {
        "read": TrackingObject.Status.COMPLETED,
        "currently-reading": TrackingObject.Status.IN_PROGRESS,
        "to-read": TrackingObject.Status.PLANNED,
    }

    def import_data(self: Self) -> None:
        csv_reader_entities, csv_reader_tracking = tee(
            csv.DictReader(self.source_file.read().decode("utf-8").splitlines())
        )
        entities = []
        for row in csv_reader_entities:
            authors = [row["Author"]]
            authors.extend(row["Additional Authors"].split(","))
            authors = [" ".join(author.split()).strip() for author in authors if author]

            publish_date = None
            if (original_publication_year := row["Original Publication Year"]) and original_publication_year.isalnum():
                publish_date = f"{original_publication_year}-01-01"

            obj = Book(
                name=row["Title"],
                author=authors,
                publish_date=publish_date,
                created_by=self.user,
                draft=True,
            )
            entities.append(obj)

        Book.objects.bulk_create(entities, ignore_conflicts=True)

        tracking_objs = []
        for row in csv_reader_tracking:
            notes = row["My Review"]
            if notes:
                notes += "\n\n"
            notes += f"Imported from Goodreads (id: {row['Book Id']})"

            obj = TrackingObject(
                content_type=ContentType.objects.get_for_model(Book),
                object_id=Book.objects.get(name=row["Title"]).pk,
                user=self.user,
                status=self.STATUS_MAPPING[row["Exclusive Shelf"]],
                rating=rating if (rating := int(row["My Rating"])) else None,
                notes=notes,
            )
            tracking_objs.append(obj)

        created_objs = TrackingObject.objects.bulk_create(tracking_objs, ignore_conflicts=True)
        logger.debug("Imported objects", extra={"created_objs": len(created_objs)})


class SimklImporter(CSVImporter):
    IMPORTER_NAME = "simkl_csv"

    STATUS_MAPPING: ClassVar = {
        "dropped": TrackingObject.Status.DROPPED,
        "watching": TrackingObject.Status.IN_PROGRESS,
        "plan to watch": TrackingObject.Status.PLANNED,
        "on hold": TrackingObject.Status.ON_HOLD,
        "completed": TrackingObject.Status.COMPLETED,
    }

    def _import_show(self: Self, row: dict[str, str]) -> None:
        release_date = f"{row['Year']}-01-01" if row["Year"] and row["Year"] != "0" else None
        return Show(
            name=row["Title"],
            release_date=release_date,
            created_by=self.user,
            draft=True,
        )

    def _import_movie(self: Self, row: dict[str, str]) -> None:
        release_date = f"{row['Year']}-01-01" if row["Year"] and row["Year"] != "0" else None
        return Movie(
            name=row["Title"],
            release_date=release_date,
            created_by=self.user,
            draft=True,
        )

    def import_data(self: Self) -> None:
        csv_reader_entities, csv_reader_tracking = tee(
            csv.DictReader(self.source_file.read().decode("utf-8").splitlines())
        )
        movies_entities = []
        shows_entities = []
        for row in csv_reader_entities:
            if row["Type"] == "movie":
                movies_entities.append(self._import_movie(row))
            else:
                shows_entities.append(self._import_show(row))

        Movie.objects.bulk_create(movies_entities, ignore_conflicts=True)
        Show.objects.bulk_create(shows_entities, ignore_conflicts=True)

        tracking_objs = []
        for row in csv_reader_tracking:
            row_model = Movie if row["Type"] == "movie" else Show

            notes = row["Memo"]
            if notes:
                notes += "\n\n"
            notes += f"Imported from Simkl (id: {row['SIMKL_ID']})"

            obj = TrackingObject(
                content_type=ContentType.objects.get_for_model(row_model),
                object_id=row_model.objects.get(name=row["Title"]).pk,
                user=self.user,
                status=self.STATUS_MAPPING[row["Watchlist"]],
                rating=int(rating) // 2 if (rating := row["Rating"]) else None,
                notes=notes,
            )
            tracking_objs.append(obj)

        created_objs = TrackingObject.objects.bulk_create(tracking_objs, ignore_conflicts=True)
        logger.debug("Imported objects", extra={"created_objs": len(created_objs)})


FRONTEND_IMPORTERS = [
    GoodreadsImporter,
    SimklImporter,
]

IMPORTER_MAPPING = {importer.IMPORTER_NAME: importer for importer in FRONTEND_IMPORTERS}
