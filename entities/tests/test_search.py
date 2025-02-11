from typing import Iterable, Self

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.test import RequestFactory, TestCase
from django.urls import reverse

from entities.factories import BookFactory, GameFactory, MovieFactory, ShowFactory
from entities.models import EntityBase
from entities.views import EntitiesSearchView

User = get_user_model()


class SearchTestCase(TestCase):
    @classmethod
    def setUpTestData(cls: type[Self]) -> None:
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(username="testuser", password="12345")  # noqa: S106

        MovieFactory(name="The Matrix")
        MovieFactory(name="The Matrix Reloaded")
        ShowFactory(name="Dexter")
        ShowFactory(name="The IT Crowd")
        GameFactory(name="The Witcher 3: Wild Hunt")
        GameFactory(name="Ghost of Tsushima")
        BookFactory(name="Atomic Habits")
        BookFactory(name="The Invincible")

    def _make_search_query(self: Self, query: str) -> str:
        request = self.factory.get(reverse("entities:entities-search"), query_params={"search": query})
        request.user = self.user

        queryset = EntitiesSearchView(request=request).get_queryset()
        return queryset

    def _assert_results_desired(self: Self, queryset: QuerySet[EntityBase], expected_results: Iterable[str]) -> None:
        self.assertCountEqual([x["name"] for x in queryset], expected_results)

    def test_search_exact_match(self: Self) -> None:
        queryset = self._make_search_query("The Witcher 3: Wild Hunt")
        self._assert_results_desired(queryset, ["The Witcher 3: Wild Hunt"])

    def test_search_partial_match(self: Self) -> None:
        queryset = self._make_search_query("Matrix")
        self._assert_results_desired(queryset, ["The Matrix Reloaded", "The Matrix"])

    def test_search_typo(self: Self) -> None:
        queryset = self._make_search_query("Dextre")
        self._assert_results_desired(queryset, ["Dexter"])

    def test_search_no_results(self: Self) -> None:
        queryset = self._make_search_query("Non-existent")
        self._assert_results_desired(queryset, [])

    def test_search_multiple_entity_types(self: Self) -> None:
        queryset = self._make_search_query("The")
        self.assertTrue(len({x["entity_type"] for x in queryset}) > 1)
