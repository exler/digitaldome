from django.urls import path

from entities.views import EntitiesDetailView, EntitiesListView

app_name = "entities"

urlpatterns = [
    path("explore/<str:entity_type>/", EntitiesListView.as_view(), name="entities-list"),
    path("explore/<str:entity_type>/<int:pk>/", EntitiesDetailView.as_view(), name="entities-detail"),
]
