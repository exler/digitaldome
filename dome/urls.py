from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.defaults import page_not_found
from django.views.generic import TemplateView

from dome.views import IndexView, ManifestView

urlpatterns = [
    *[
        path("admin/", admin.site.urls),
        path("", IndexView.as_view(), name="index"),
        path("manifest.json", ManifestView.as_view(), name="manifest"),
        path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
        path("", include("users.urls")),
        path("entities/", include("entities.urls")),
        path("user/", include("tracking.urls")),
        path("integrations/", include("integrations.urls")),
    ],
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

if settings.DEBUG:
    urlpatterns = [*[path("404/", page_not_found, kwargs={"exception": Exception("Debug exception")}), *urlpatterns]]
