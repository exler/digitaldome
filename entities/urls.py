from django.urls import path

from entities.views import (
    ApprovalListView,
    ApproveEntityView,
    DraftsListView,
    EntitiesCreateChooseView,
    EntitiesCreateView,
    EntitiesDetailView,
    EntitiesListView,
    EntitiesUpdateView,
)

app_name = "entities"

urlpatterns = [
    path("drafts/", DraftsListView.as_view(), name="drafts-list"),
    path("approvals/", ApprovalListView.as_view(), name="approvals-list"),
    path("add/", EntitiesCreateChooseView.as_view(), name="entities-create-choose"),
    path("add/<str:entity_type>/", EntitiesCreateView.as_view(), name="entities-create"),
    path("update/<str:entity_type>/<int:pk>/", EntitiesUpdateView.as_view(), name="entities-update"),
    path("approve/<str:entity_type>/<int:pk>/", ApproveEntityView.as_view(), name="entities-approve"),
    path("<str:entity_type>/", EntitiesListView.as_view(), name="entities-list"),
    path("<str:entity_type>/<int:pk>/", EntitiesDetailView.as_view(), name="entities-detail"),
]
