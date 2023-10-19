from typing import Any, Self

from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from entities.mappings import get_model_from_entity_type
from entities.models import EntityBase
from tracking.models import TrackingObject


class TrackingObjectMixin:
    model = TrackingObject

    def _get_entity(self: Self) -> type[EntityBase]:
        entity_type = self.kwargs["entity_type"]
        entity_type_model = get_model_from_entity_type(entity_type)
        entity = get_object_or_404(entity_type_model, pk=self.kwargs["pk"])
        return entity

    def dispatch(self: Self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.entity = self._get_entity()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self: Self, queryset: QuerySet[TrackingObject] | None = None) -> TrackingObject:
        if queryset is None:
            queryset = self.get_queryset()

        try:
            return queryset.get(
                content_type=ContentType.objects.get_for_model(self.entity),
                object_id=self.entity.pk,
                user=self.request.user,
            )
        except TrackingObject.DoesNotExist:
            raise Http404
