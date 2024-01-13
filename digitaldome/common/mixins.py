from typing import Any, ClassVar, Self

from django.core.paginator import Page
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


class ElidedPaginationMixin:
    """
    Adds the `adjusted_elided_pages` to the template context's `page_obj`.

    Use with `{% include "partials/pagination.html" %}`.
    """

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_object: Page = context["page_obj"]
        page_object.adjusted_elided_pages = page_object.paginator.get_elided_page_range(
            page_object.number, on_each_side=2
        )
        context["page_obj"] = page_object
        return context
