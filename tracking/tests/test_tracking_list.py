from typing import Self

from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.test import TestCase
from django.urls import reverse

from entities.factories import MovieFactory
from tracking.models import TrackingObject

User = get_user_model()


class TrackingListViewOrderingTestCase(TestCase):
    """Tests for TrackingListView ordering functionality, especially entity_name ordering."""

    @classmethod
    def setUpTestData(cls: type[Self]) -> None:
        cls.user = User.objects.create_user(username="testuser", password="12345")  # noqa: S106

        # Create movies with specific names for alphabetical ordering tests
        cls.movie_alpha = MovieFactory(name="Alpha Movie")
        cls.movie_beta = MovieFactory(name="Beta Movie")
        cls.movie_zulu = MovieFactory(name="Zulu Movie")

        # Create tracking objects for the user
        cls.tracking_alpha = TrackingObject.objects.create(
            user=cls.user,
            content_object=cls.movie_alpha,
            status=TrackingObject.Status.IN_PROGRESS,
            rating=3,
        )
        cls.tracking_beta = TrackingObject.objects.create(
            user=cls.user,
            content_object=cls.movie_beta,
            status=TrackingObject.Status.IN_PROGRESS,
            rating=5,
        )
        cls.tracking_zulu = TrackingObject.objects.create(
            user=cls.user,
            content_object=cls.movie_zulu,
            status=TrackingObject.Status.IN_PROGRESS,
            rating=1,
        )

    def setUp(self: Self) -> None:
        self.client.force_login(self.user)

    def _get_tracking_list_url(self: Self, ordering: str | None = None) -> str:
        url = reverse("tracking:tracking-list", kwargs={"username": self.user.username, "entity_type": "movie"})
        if ordering:
            url += f"?ordering={ordering}"
        return url

    def _get_tracking_names_from_response(self: Self, response: HttpResponse) -> list[str]:
        """Extract entity names from the tracking objects in the response context."""
        return [obj.content_object.name for obj in response.context["object_list"]]

    def test_ordering_by_entity_name_ascending(self: Self) -> None:
        """Test that ordering by entity_name (ascending) works correctly."""
        response = self.client.get(self._get_tracking_list_url(ordering="entity_name"))

        self.assertEqual(response.status_code, 200)
        names = self._get_tracking_names_from_response(response)
        self.assertEqual(names, ["Alpha Movie", "Beta Movie", "Zulu Movie"])

    def test_ordering_by_entity_name_descending(self: Self) -> None:
        """Test that ordering by entity_name (descending) works correctly."""
        response = self.client.get(self._get_tracking_list_url(ordering="-entity_name"))

        self.assertEqual(response.status_code, 200)
        names = self._get_tracking_names_from_response(response)
        self.assertEqual(names, ["Zulu Movie", "Beta Movie", "Alpha Movie"])

    def test_ordering_by_rating_ascending(self: Self) -> None:
        """Test that ordering by rating (ascending) works correctly."""
        response = self.client.get(self._get_tracking_list_url(ordering="rating"))

        self.assertEqual(response.status_code, 200)
        ratings = [obj.rating for obj in response.context["object_list"]]
        self.assertEqual(ratings, [1, 3, 5])

    def test_ordering_by_rating_descending(self: Self) -> None:
        """Test that ordering by rating (descending) works correctly."""
        response = self.client.get(self._get_tracking_list_url(ordering="-rating"))

        self.assertEqual(response.status_code, 200)
        ratings = [obj.rating for obj in response.context["object_list"]]
        self.assertEqual(ratings, [5, 3, 1])
