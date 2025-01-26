from typing import Any, Self

from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
from django.db.models.expressions import Value
from django.views.generic import DetailView, ListView
from django_filters.filterset import FilterSet
from django_filters.views import FilterView

from digitaldome.common.mixins import ElidedPaginationMixin
from entities.filters import EntitySearchFilter
from entities.mappings import ENTITY_MODEL_TO_FILTER_MAPPING
from entities.mixins import DynamicEntityMixin
from entities.models import Book, EntityBase, Game, Movie, Show
from tracking.models import TrackingObject


class EntitiesListView(ElidedPaginationMixin, DynamicEntityMixin, FilterView):
    """
    View for rendering a list of entities of a type passed in the URL.
    """

    template_name = "entities/entities_list.html"

    paginate_by = 20

    def get_filterset_class(self: Self) -> type[FilterSet]:
        return ENTITY_MODEL_TO_FILTER_MAPPING[self.model]

    def get_queryset(self: Self) -> QuerySet[EntityBase]:
        """
        Get queryset based on entity type passed in URL.
        """

        return super().get_queryset()


class EntitiesDetailView(DynamicEntityMixin, DetailView):
    template_name = "entities/entities_detail.html"

    def get_queryset(self: Self) -> QuerySet[EntityBase]:
        """
        Get queryset based on entity type passed in URL.
        """

        return super().get_queryset()

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            try:
                tracking_obj = TrackingObject.objects.get(
                    object_id=self.object.id,
                    content_type=ContentType.objects.get_for_model(self.object),
                    user=self.request.user,
                )
            except TrackingObject.DoesNotExist:
                tracking_obj = None
        else:
            tracking_obj = None

        context["tracking_obj"] = tracking_obj
        return context


class EntitiesSearchView(ListView):
    template_name = "entities/entities_search.html"

    def _prepare_queryset(self, model: type[EntityBase]) -> QuerySet[EntityBase]:
        return EntitySearchFilter(
            self.request.GET,
            queryset=model.objects.annotate(entity_type=Value(model._meta.verbose_name)),
        ).qs.values("id", "name", "image", "entity_type", "rank")

    def get_queryset(self) -> QuerySet[EntityBase]:
        """
        Overriding `get_queryset` with filters because it is not possible
        to use `.annotate` (required for the ranking) after `.union`.
        """

        if not self.request.GET.get("search"):
            # If no search query is provided, just return an empty list
            # to focus on rendering the page
            return []

        movie_qs = self._prepare_queryset(Movie)
        show_qs = self._prepare_queryset(Show)
        game_qs = self._prepare_queryset(Game)
        book_qs = self._prepare_queryset(Book)

        # Combine all querysets using union
        unified_qs = movie_qs.union(show_qs, game_qs, book_qs)

        # Return the combined queryset
        return unified_qs[:20]
