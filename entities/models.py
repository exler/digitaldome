from typing import ClassVar, Self

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.files import File
from django.db import models
from django.db.models.functions import Lower
from django.db.models.query_utils import Q
from django.templatetags.static import static
from django.urls import reverse
from django.utils.functional import cached_property

from digitaldome.common.models import TimestampedModel
from digitaldome.utils.image import resize_and_crop_image
from entities.helpers import format_time_spent
from users.models import User


class Tag(TimestampedModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self: Self) -> str:
        return self.name


class EntityQueryset(models.QuerySet):
    def visible_for_user(self: Self, user: User) -> Self:
        return self.filter(Q(created_by=user) | Q(approved=True))


def image_upload_destination(instance: object, filename: str) -> str:
    return f"entities/{instance.__class__.__name__.lower()}s/{filename}"


class EntityBase(TimestampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to=image_upload_destination, null=True, blank=True)

    wikipedia_url = models.URLField(blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
    )

    # Incomplete object that is only visible to the creating user.
    # Can be completed by the user themselves.
    draft = models.BooleanField(default=False)

    # Visible to the creating user only and moderator/admin.
    # Waiting for approval from moderator/admin.
    approved = models.BooleanField(default=False)

    # Fields that are shown in the detail view.
    # Their HTML representation can be configured with a function named
    # `get_<field_name>_display` on the model.
    ADDITIONAL_DETAIL_FIELDS: tuple[str] = ()

    objects = EntityQueryset.as_manager()

    IMAGE_WIDTH = 192
    IMAGE_HEIGHT = 288

    class Meta:
        abstract = True
        constraints: ClassVar = [
            models.UniqueConstraint(Lower("name"), name="%(class)s_unique_name"),
        ]

    def get_absolute_url(self: Self) -> str:
        return reverse("entities:entities-detail", kwargs={"entity_type": self._meta.verbose_name, "pk": self.pk})

    @property
    def requires_approval(self: Self) -> bool:
        return not self.draft and not self.approved

    @cached_property
    def image_url(self: Self) -> str | None:
        """
        Gets image URL to display or a placeholder if no image is available.
        """
        if self.image:
            return self.image.url
        return static("img/image-placeholder.png")

    def save_image(self: Self, source_file: File) -> None:
        """
        Saves the image file to the upload target under the file's name.
        Automatically crops the image to the desired size.
        """
        image_file = resize_and_crop_image(source_file, self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        self.image.save(image_file.name, image_file, save=False)


class Identity(EntityBase):
    birth_date = models.DateField(null=True, blank=True)

    ADDITIONAL_DETAIL_FIELDS = ("birth_date",)

    def __str__(self: Self) -> str:
        return self.name


class Movie(EntityBase):
    release_date = models.DateField(null=True, blank=True)

    length = models.PositiveSmallIntegerField(null=True, blank=True)  # In minutes

    director = models.ManyToManyField(Identity, related_name="directed_movies", blank=True)
    cast = models.ManyToManyField(Identity, related_name="acted_in_movies", blank=True)

    ADDITIONAL_DETAIL_FIELDS = ("release_date", "length", "director", "cast")

    def __str__(self: Self) -> str:
        return f"{self.name} ({self.release_date.year})"

    def get_length_display(self: Self) -> str:
        if not self.length:
            return "n/a"

        return format_time_spent(self.length)


class Show(EntityBase):
    release_date = models.DateField(null=True, blank=True)

    creator = models.ManyToManyField(Identity, related_name="created_shows", blank=True)
    stars = models.ManyToManyField(Identity, related_name="starred_in_shows", blank=True)

    ADDITIONAL_DETAIL_FIELDS = ("release_date", "creator", "stars")

    def __str__(self: Self) -> str:
        return self.name


class Game(EntityBase):
    release_date = models.DateField(null=True, blank=True)

    platforms = ArrayField(models.CharField(max_length=255), default=list, blank=True)

    producer = models.ManyToManyField(Identity, related_name="produced_games", blank=True)
    publisher = models.ManyToManyField(Identity, related_name="published_games", blank=True)

    ADDITIONAL_DETAIL_FIELDS = ("release_date", "platforms", "producer", "publisher")

    def __str__(self: Self) -> str:
        return self.name


class Book(EntityBase):
    publish_date = models.DateField(null=True, blank=True)

    author = models.ManyToManyField(Identity, related_name="written_books", blank=True)

    ADDITIONAL_DETAIL_FIELDS = ("publish_date", "author")

    def __str__(self: Self) -> str:
        return self.name
