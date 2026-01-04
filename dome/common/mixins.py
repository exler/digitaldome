from typing import Any, ClassVar, Iterable, Self

from django.core.paginator import Page
from django.db.models import F
from django.utils.datastructures import MultiValueDict
from django_filters.filterset import FilterSet


class DynamicOrderingMixin:
    """
    Adds the ability to dynamically order the queryset based on the `ordering` GET parameter.

    Example usage:
    ```
    class MyView(DynamicOrderingMixin, ListView):
        ordering_fields = ["name", "-created_at"]
    ```

    The above example would allow the user to order the queryset
    by `name` (ASC) or `created_at` (DESC) by passing the `order_by` GET parameter.
    """

    ordering_fields: ClassVar[Iterable[str]] = []

    def get_queryset(self: Self) -> Any:
        queryset = super().get_queryset()
        return self.order_queryset(queryset)

    def get_ordering(self: Self) -> str:
        ordering = self.request.GET.get("ordering")

        if ordering in self.ordering_fields:
            return ordering

        return None

    def order_queryset(self: Self, queryset: Any) -> Any:
        if ordering := self.get_ordering():
            if ordering.startswith("-"):
                field = ordering[1:]
                return queryset.order_by(F(field).desc(nulls_last=True))
            else:
                return queryset.order_by(F(ordering).asc(nulls_first=True))
        return queryset

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ordering"] = self.get_ordering()
        return context


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
