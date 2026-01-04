from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views.generic import RedirectView, View


class IndexView(RedirectView):
    url = reverse_lazy("users:login")


class ManifestView(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        data = {
            "name": "Dome",
            "short_name": "Dome",
            "description": "Comprehensive media tracker",
            "start_url": "/",
            "display": "standalone",
            "icons": [
                {
                    "src": static("android-chrome-192x192.png"),
                    "sizes": "192x192",
                    "type": "image/png",
                },
                {
                    "src": static("android-chrome-512x512.png"),
                    "sizes": "512x512",
                    "type": "image/png",
                },
            ],
        }

        return JsonResponse(data)
