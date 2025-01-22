from typing import Any, Self

from django.http import HttpRequest

from entities.mappings import get_model_from_entity_type


class DynamicEntityMixin:
    def setup(self: Self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        self.model = get_model_from_entity_type(self.kwargs["entity_type"])

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["entity_type"] = self.kwargs["entity_type"]
        return context
