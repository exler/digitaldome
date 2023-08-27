from typing import Any, Self

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import DetailView, ListView

from entities.models import EntityBase
from entities.utils import get_model_from_entity_type


class EntitiesListView(LoginRequiredMixin, ListView):
    """
    View for rendering a list of entities of a type passed in the URL.
    """

    template_name = "entities/entities_list.html"

    def get_queryset(self: Self) -> QuerySet[EntityBase]:
        """
        Get queryset based on entity type passed in URL.
        """

        self.model = get_model_from_entity_type(self.kwargs["entity_type"])
        return super().get_queryset()

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.kwargs["entity_type"].capitalize()
        return context


class EntitiesDetailView(LoginRequiredMixin, DetailView):
    template_name = "entities/entities_detail.html"

    def get_queryset(self: Self) -> QuerySet[EntityBase]:
        """
        Get queryset based on entity type passed in URL.
        """

        self.model = get_model_from_entity_type(self.kwargs["entity_type"])
        return super().get_queryset()
