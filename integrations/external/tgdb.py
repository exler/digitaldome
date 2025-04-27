from io import BytesIO

import requests
from django.conf import settings


class TGDBClient:
    API_CLIENT_ID = settings.TGDB_API_CLIENT_ID
    API_CLIENT_SECRET = settings.TGDB_API_CLIENT_SECRET

    AUTH_URL = "https://id.twitch.tv/oauth2/token"

    BASE_API_URL = "https://api.igdb.com/v4"

    def __init__(self) -> None:
        self.session = requests.Session()

    def get_access_token(self) -> str:
        url = self.AUTH_URL
        url += f"?client_id={self.API_CLIENT_ID}"
        url += f"&client_secret={self.API_CLIENT_SECRET}"
        url += "&grant_type=client_credentials"

        response = requests.post(url, timeout=5)
        return response.json().get("access_token")

    def search(self, query: str) -> dict:
        url = f"{self.BASE_API_URL}/games"

        headers = {
            "Accept": "application/json",
            "Client-ID": self.API_CLIENT_ID,
            "Authorization": f"Bearer {self.get_access_token()}",
        }

        data = f'search "{query}";'
        data += "fields name, cover.image_id, first_release_date, platforms.name, summary, genres.name, "
        data += "websites.type.type, websites.url, "
        data += "involved_companies.developer, involved_companies.publisher, involved_companies.company.name;"
        data += "limit 1;"

        response = self.session.post(url, headers=headers, data=data, timeout=5)
        return response.json()

    def get_cover_image(self, image_id: str) -> BytesIO:
        url = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{image_id}.webp"

        response = self.session.get(url, timeout=5)
        return BytesIO(response.content)


tgdb_client = TGDBClient()
