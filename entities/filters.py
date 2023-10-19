from typing import ClassVar, Self

import django_filters
from django.db.models import QuerySet
from django_filters.filterset import FilterSet

from entities.models import Book, EntityBase, Game, Identity, Movie, Show


class EntityBaseFilter(FilterSet):
    search = django_filters.CharFilter(method="search_filter")

    class Meta:
        fields: ClassVar = ["search"]

    def search_filter(self: Self, queryset: QuerySet[EntityBase], name: str, value: str) -> QuerySet[EntityBase]:
        return queryset.filter(name__icontains=value)


class IdentityFilter(EntityBaseFilter):
    class Meta(EntityBaseFilter.Meta):
        model = Identity


class MovieFilter(EntityBaseFilter):
    class Meta(EntityBaseFilter.Meta):
        model = Movie


class ShowFilter(EntityBaseFilter):
    class Meta(EntityBaseFilter.Meta):
        model = Show


class GameFilter(EntityBaseFilter):
    class Meta(EntityBaseFilter.Meta):
        model = Game


class BookFilter(EntityBaseFilter):
    class Meta(EntityBaseFilter.Meta):
        model = Book
