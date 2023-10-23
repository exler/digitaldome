from django.urls import path

from integrations.views import ExportTrackingDataView, ImportTrackingDataView

app_name = "integrations"

urlpatterns = [
    path("import/", ImportTrackingDataView.as_view(), name="import-tracking-data"),
    path("export/", ExportTrackingDataView.as_view(), name="export-tracking-data"),
]
