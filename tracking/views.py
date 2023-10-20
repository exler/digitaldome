from typing import Any, ClassVar, Dict, Self

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import DeleteView, ModelFormMixin, ProcessFormView
from django_filters.filterset import FilterSet
from django_filters.views import FilterView

from digitaldome.common.mixins import DefaultFilterMixin
from entities.helpers import format_time_spent
from entities.mappings import get_model_from_entity_type
from tracking.forms import TrackingObjectForm
from tracking.mixins import TrackingObjectMixin
from tracking.models import TrackingObject, UserStats


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "tracking/dashboard.html"

    def get_context_data(self: Self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tracking_objects = TrackingObject.objects.filter(user=self.request.user).prefetch_related("content_object")
        context["completed_list"] = tracking_objects.filter(status=TrackingObject.Status.COMPLETED).order_by(
            "-updated_at"
        )[:5]
        context["in_progress_list"] = tracking_objects.filter(status=TrackingObject.Status.IN_PROGRESS).order_by(
            "-updated_at"
        )[:5]
        return context


class TrackingFilter(FilterSet):
    class Meta:
        model = TrackingObject
        fields: ClassVar = ["status"]


class TrackingListView(LoginRequiredMixin, DefaultFilterMixin, FilterView):
    template_name = "tracking/tracking_list.html"
    paginate_by = 20
    filterset_class = TrackingFilter

    default_filter_values: ClassVar = {"status": TrackingObject.Status.IN_PROGRESS}

    def get_queryset(self: Self) -> QuerySet[TrackingObject]:
        entity_type = get_model_from_entity_type(self.kwargs["entity_type"])
        content_type = ContentType.objects.get_for_model(entity_type)
        return TrackingObject.objects.filter(user=self.request.user, content_type=content_type)

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["entity_type"] = self.kwargs["entity_type"]
        return context


class StatsView(LoginRequiredMixin, DetailView):
    template_name = "tracking/stats.html"

    def get_object(self: Self, queryset: QuerySet[UserStats] | None = None) -> UserStats:
        return UserStats.objects.get_or_create(user=self.request.user)[0]

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["time_spent_on_movies"] = format_time_spent(self.object.time_spent_on_movies)
        return context


class TrackingFormView(LoginRequiredMixin, TrackingObjectMixin, ModelFormMixin, ProcessFormView):
    form_class = TrackingObjectForm

    def post(self: Self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            self.object = self.get_object()
        except Http404:
            self.object = None

        return super().post(request, *args, **kwargs)

    def form_valid(self: Self, form: ModelForm) -> HttpResponse:
        self.object = form.save()
        return render(
            self.request, "entities/entities_detail.html", {"object": self.entity, "tracking_obj": self.object}
        )

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


class TrackingDeleteView(LoginRequiredMixin, TrackingObjectMixin, DeleteView):
    model = TrackingObject

    def delete(self: Self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        self.object.delete()
        return render(self.request, "entities/entities_detail.html", {"object": self.entity})
