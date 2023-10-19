from django.urls import path

from tracking.views import (
    DashboardView,
    StatsView,
    TrackingDeleteView,
    TrackingFormView,
    TrackingListView,
)

app_name = "tracking"

urlpatterns = [
    path("<int:user_id>/dashboard/", DashboardView.as_view(), name="dashboard"),
    path("<int:user_id>/stats/", StatsView.as_view(), name="stats"),
    path("<int:user_id>/<str:entity_type>/", TrackingListView.as_view(), name="tracking-list"),
    path("track/<str:entity_type>/<int:pk>/", TrackingFormView.as_view(), name="track"),
    path("stop-tracking/<str:entity_type>/<int:pk>/", TrackingDeleteView.as_view(), name="tracking-delete"),
]
