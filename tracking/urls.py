from django.urls import path

from tracking.views import (
    DashboardView,
    TrackingDeleteView,
    TrackingFormView,
    TrackingListView,
)

app_name = "tracking"

urlpatterns = [
    path("@<str:username>/dashboard/", DashboardView.as_view(), name="dashboard"),
    path("@<str:username>/<str:entity_type>/", TrackingListView.as_view(), name="tracking-list"),
    path("track/<str:entity_type>/<int:pk>/", TrackingFormView.as_view(), name="track"),
    path("stop-tracking/<str:entity_type>/<int:pk>/", TrackingDeleteView.as_view(), name="tracking-delete"),
]
