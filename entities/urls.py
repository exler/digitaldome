from django.urls import path

from entities.views import (
    EntitiesCreateChooseView,
    EntitiesCreateView,
    EntitiesDetailView,
    EntitiesListView,
    EntitiesUpdateView,
)

app_name = "entities"

urlpatterns = [
    path("add/", EntitiesCreateChooseView.as_view(), name="entities-create-choose"),
    path("add/<str:entity_type>/", EntitiesCreateView.as_view(), name="entities-create"),
    path("update/<str:entity_type>/<int:pk>/", EntitiesUpdateView.as_view(), name="entities-update"),
    path("<str:entity_type>/", EntitiesListView.as_view(), name="entities-list"),
    path("<str:entity_type>/<int:pk>/", EntitiesDetailView.as_view(), name="entities-detail"),
]
