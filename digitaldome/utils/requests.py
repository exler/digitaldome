import httpx
from django.core.files.base import ContentFile, File


def download_file(url: str, filename: str | None = None, client: httpx.Client | None = None) -> File:
    """Download image from URL and return Django file."""

    filename = filename or url.split("/")[-1]

    response = client.get(url) if client else httpx.get(url)
    response.raise_for_status()

    return ContentFile(response.content, name=filename)
