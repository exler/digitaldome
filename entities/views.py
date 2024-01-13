from typing import Any, Self

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Count, QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView, View
from django_filters.filterset import FilterSet
from django_filters.views import FilterView

from digitaldome.common.mixins import ElidedPaginationMixin
from entities.mappings import ENTITY_MODEL_TO_FILTER_MAPPING, ENTITY_MODEL_TO_FORM_MAPPING, get_model_from_entity_type
from entities.mixins import DynamicEntityMixin, ModeratorOnlyMixin
from entities.models import EntityBase
from tracking.models import TrackingObject


class EntitiesListView(ElidedPaginationMixin, DynamicEntityMixin, LoginRequiredMixin, FilterView):
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

        return super().get_queryset().visible_for_user(self.request.user)


class EntitiesDetailView(DynamicEntityMixin, LoginRequiredMixin, DetailView):
    template_name = "entities/entities_detail.html"

    def get_queryset(self: Self) -> QuerySet[EntityBase]:
        """
        Get queryset based on entity type passed in URL.
        """

        return super().get_queryset().visible_for_user(self.request.user)

    def _get_entity_stats(self: Self) -> dict[str, Any]:
        stats = {}
        ratings = TrackingObject.objects.filter(
            object_id=self.object.id,
            content_type=ContentType.objects.get_for_model(self.object),
            rating__isnull=False,
        ).aggregate(Avg("rating"), Count("rating"))
        stats["digitaldome_rating"] = ratings["rating__avg"]
        stats["digitaldome_rating_count"] = ratings["rating__count"]
        return stats

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        try:
            tracking_obj = TrackingObject.objects.get(
                object_id=self.object.id,
                content_type=ContentType.objects.get_for_model(self.object),
                user=self.request.user,
            )
        except TrackingObject.DoesNotExist:
            tracking_obj = None

        context["tracking_obj"] = tracking_obj
        context["entity_stats"] = self._get_entity_stats()
        return context


class EntitiesCreateChooseView(LoginRequiredMixin, TemplateView):
    template_name = "entities/entities_create_choose.html"

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        entity_types = [(model._meta.verbose_name, model.COLOR) for model in EntityBase.__subclasses__()]
        context["entity_types"] = entity_types
        return context


class EntitiesCreateView(DynamicEntityMixin, LoginRequiredMixin, CreateView):
    template_name = "entities/entities_changeform.html"

    def get_form_kwargs(self: Self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_form_class(self: Self) -> type[BaseModelForm]:
        return ENTITY_MODEL_TO_FORM_MAPPING[self.model]


class EntitiesUpdateView(DynamicEntityMixin, LoginRequiredMixin, UpdateView):
    template_name = "entities/entities_changeform.html"

    def get_form_kwargs(self: Self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_form_class(self: Self) -> type[BaseModelForm]:
        return ENTITY_MODEL_TO_FORM_MAPPING[self.model]


class DraftsListView(LoginRequiredMixin, TemplateView):
    template_name = "entities/user_entities_list.html"

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = "My Drafts"

        object_list = []
        for subclass in EntityBase.__subclasses__():
            object_list.extend(list(subclass.objects.visible_for_user(self.request.user).filter(draft=True)))

        context["object_list"] = object_list
        return context


class ApprovalListView(ModeratorOnlyMixin, LoginRequiredMixin, TemplateView):
    template_name = "entities/user_entities_list.html"

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Approval List"

        object_list = []
        for subclass in EntityBase.__subclasses__():
            object_list.extend(
                list(subclass.objects.visible_for_user(self.request.user).filter(draft=False, approved=False))
            )

        context["object_list"] = object_list
        return context


class ApproveEntityView(ModeratorOnlyMixin, LoginRequiredMixin, View):
    def post(self: Self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        model = get_model_from_entity_type(self.kwargs["entity_type"])
        entity = get_object_or_404(model, pk=self.kwargs["pk"])
        entity.approved = True
        entity.save(update_fields=["approved"])
        return redirect("entities:entities-detail", entity_type=self.kwargs["entity_type"], pk=self.kwargs["pk"])
