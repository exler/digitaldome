from typing import Any, Self

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from users.forms import SettingsForm
from users.models import User


class SettingsView(LoginRequiredMixin, UpdateView):
    template_name = "users/settings.html"

    form_class = SettingsForm

    success_url = reverse_lazy("users:settings")

    def get_object(self: Self, queryset: QuerySet[Any] = None) -> User:
        return self.request.user
