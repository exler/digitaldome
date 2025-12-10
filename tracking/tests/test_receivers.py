from django.contrib.auth import get_user_model
from django.test import TestCase

from entities.factories import MovieFactory
from tracking.models import TrackingObject

User = get_user_model()


class TestReceivers(TestCase):
    """Tests for receivers in the tracking app."""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="testuser", password="12345")  # noqa: S106

    def test_tracking_object_deleted_when_entity_deleted(self) -> None:
        """Test that a TrackingObject is deleted when its associated entity is deleted."""

        movie = MovieFactory()
        tracking_object = TrackingObject.objects.create(
            user=self.user,
            content_object=movie,
            status=TrackingObject.Status.IN_PROGRESS,
            rating=4,
        )

        with self.captureOnCommitCallbacks(execute=True):
            # Delete the associated entity
            movie.delete()

        # Ensure the TrackingObject has been deleted
        self.assertFalse(TrackingObject.objects.filter(id=tracking_object.id).exists())
