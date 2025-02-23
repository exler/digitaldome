import csv
import logging
from typing import Any, Generator, Iterator, Self

from django.http import StreamingHttpResponse

from tracking.models import TrackingObject
from users.models import User

logger = logging.getLogger(__name__)


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self: Self, value: Any) -> Any:
        """Write the value by returning it, instead of storing in a buffer."""
        return value


class Exporter:
    def __init__(self: Self, user: User, output_filename: str) -> None:
        self.user = user
        self.output_filename = output_filename

    def get_objects_iterator(self: Self) -> Iterator[TrackingObject]:
        return (
            TrackingObject.objects.filter(user=self.user).prefetch_related("content_object").iterator(chunk_size=1000)
        )

    def get_headers_row(self: Self) -> list[str]:
        return ["Title", "Type", "Status", "Rating", "Notes"]

    def get_rows(self: Self) -> Generator[list[str], None, None]:
        objects = self.get_objects_iterator()

        yield self.get_headers_row()

        for obj in objects:
            yield self.get_row(obj)

    def get_row(self: Self, obj: TrackingObject) -> list[str]:
        content_object = obj.content_object

        return [
            content_object.name,
            content_object.__class__.__name__.title(),
            obj.get_status_display(),
            str(obj.rating),
            obj.notes,
        ]

    def get_streaming_response(self: Self) -> StreamingHttpResponse:
        buffer = Echo()
        writer = csv.writer(buffer)
        return StreamingHttpResponse(
            (writer.writerow(row) for row in self.get_rows()),
            content_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{self.output_filename}.csv"'},
        )
