from typing import Any, ClassVar, Self

from django.utils.datastructures import MultiValueDict
from django_filters.filterset import FilterSet


class DefaultFilterMixin:
    default_filter_values: ClassVar = {}

    def get_filterset_kwargs(self: Self, filterset_class: type[FilterSet]) -> dict[str, Any]:
        kwargs = super().get_filterset_kwargs(filterset_class)
        filter_values = MultiValueDict() if kwargs["data"] is None else kwargs["data"].copy()

        for key, value in self.default_filter_values.items():
            if key not in filter_values:
                if isinstance(value, list):
                    filter_values.setlist(key, value)
                else:
                    filter_values[key] = value

        kwargs["data"] = filter_values
        return kwargs
