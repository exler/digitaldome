from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.defaults import page_not_found

from digitaldome.views import IndexView

urlpatterns = [
    *[
        path("admin/", admin.site.urls),
        path("", IndexView.as_view(), name="index"),
        path("", include("users.urls")),
        path("", include("entities.urls")),
        path("", include("tracking.urls")),
    ],
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

if settings.DEBUG:
    urlpatterns += [path("404/", page_not_found, kwargs={"exception": Exception("Debug exception")})]
