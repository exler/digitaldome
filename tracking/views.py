from typing import Any, Dict, Self, Type

from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
from django.http import Http404
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView, SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django.views.generic.list import ListView

from entities.models import EntityBase
from entities.utils import get_model_from_entity_type
from tracking.forms import TrackingObjectForm
from tracking.models import TrackingObject


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "tracking/dashboard.html"

    def get_context_data(self: Self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tracking_objects = TrackingObject.objects.filter(user=self.request.user)
        context["completed_list"] = tracking_objects.filter(status=TrackingObject.Status.COMPLETED)
        context["in_progress_list"] = tracking_objects.filter(status=TrackingObject.Status.IN_PROGRESS)
        return context


class TrackingListView(LoginRequiredMixin, ListView):
    template_name = "tracking/tracking_list.html"
    paginate_by = 10

    def get_queryset(self: Self) -> QuerySet[TrackingObject]:
        entity_type = get_model_from_entity_type(self.kwargs["entity_type"])
        content_type = ContentType.objects.get_for_model(entity_type)
        return TrackingObject.objects.filter(user=self.request.user, content_type=content_type)

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.kwargs["entity_type"].capitalize()
        return context


class TrackingDetailView(LoginRequiredMixin, DetailView):
    template_name = "tracking/tracking_detail.html"

    def get_queryset(self: Self) -> QuerySet[TrackingObject]:
        entity_type = get_model_from_entity_type(self.kwargs["entity_type"])
        content_type = ContentType.objects.get_for_model(entity_type)
        return TrackingObject.objects.filter(user=self.request.user, content_type=content_type)


class StatsView(LoginRequiredMixin, TemplateView):
    template_name = "tracking/stats.html"


class TrackingFormView(LoginRequiredMixin, SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    template_name = "tracking/tracking_changeform.html"
    form_class = TrackingObjectForm
    model = TrackingObject

    def _get_entity(self: Self) -> Type[EntityBase]:
        entity_type = self.kwargs["entity_type"]
        entity_type_model = get_model_from_entity_type(entity_type)
        entity = get_object_or_404(entity_type_model, pk=self.kwargs["pk"])
        return entity

    def dispatch(self: Self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
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

    def get(self: Self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            self.object = self.get_object()
        except Http404:
            self.object = None

        return super().get(request, *args, **kwargs)

    def post(self: Self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            self.object = self.get_object()
        except Http404:
            self.object = None

        return super().post(request, *args, **kwargs)

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["entity"] = self.entity
        return context

    def get_form_kwargs(self: Self) -> dict[str, Any]:
        form_kwargs = super().get_form_kwargs()
        form_kwargs["entity"] = self.entity
        if self.request.user.is_authenticated:
            form_kwargs["user"] = self.request.user
        return form_kwargs

    def get_success_url(self: Self) -> str:
        return reverse(
            "entities:entities-detail", kwargs={"entity_type": self.kwargs["entity_type"], "pk": self.kwargs["pk"]}
        )
