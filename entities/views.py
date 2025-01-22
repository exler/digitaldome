from typing import Any, Self

from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
from django.views.generic import DetailView
from django_filters.filterset import FilterSet
from django_filters.views import FilterView

from digitaldome.common.mixins import ElidedPaginationMixin
from entities.mappings import ENTITY_MODEL_TO_FILTER_MAPPING
from entities.mixins import DynamicEntityMixin
from entities.models import EntityBase
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
