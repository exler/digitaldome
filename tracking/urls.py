from django.urls import path

from tracking.views import (
    DashboardView,
    StatsView,
    TrackingDetailView,
    TrackingFormView,
    TrackingListView,
)

app_name = "tracking"

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("stats/", StatsView.as_view(), name="stats"),
    path("<str:entity_type>/", TrackingListView.as_view(), name="tracking-list"),
    path("<str:entity_type>/<int:pk>/", TrackingDetailView.as_view(), name="tracking-detail"),
    path("track/<str:entity_type>/<int:pk>/", TrackingFormView.as_view(), name="track"),
]
