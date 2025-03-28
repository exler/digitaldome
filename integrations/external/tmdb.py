from enum import StrEnum
from io import BytesIO

import requests
from django.conf import settings


class TMDBSupportedEntityType(StrEnum):
    MOVIE = "movie"
    SHOW = "tv"


class TMDBClient:
    API_KEY = settings.TMDB_API_KEY

    BASE_API_URL = "https://api.themoviedb.org/3"

    IMAGE_SECURE_BASE_URL = "https://image.tmdb.org/t/p"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "accept": "application/json",
                "Authorization": f"Bearer {self.API_KEY}",
            }
        )

    def search(self, entity_type: TMDBSupportedEntityType, query: str) -> dict:
        url = f"{self.BASE_API_URL}/search/{entity_type}?query={query}&include_adult=false&language=en-US&page=1"

        response = self.session.get(url, timeout=5)
        return response.json()

    def get_details(self, entity_type: TMDBSupportedEntityType, entity_id: int) -> dict:
        url = f"{self.BASE_API_URL}/{entity_type}/{entity_id}"

        response = self.session.get(url, timeout=5)
        return response.json()

    def get_image(self, size: str, path: str) -> BytesIO:
        url = f"{self.IMAGE_SECURE_BASE_URL}/{size}{path}"

        response = self.session.get(url, timeout=5)
        return BytesIO(response.content)


tmdb_client = TMDBClient()
