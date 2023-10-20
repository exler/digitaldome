from django.urls import path

from integrations.views import ImportTrackingDataView

app_name = "integrations"

urlpatterns = [
    path("import/", ImportTrackingDataView.as_view(), name="import-tracking-data"),
]
