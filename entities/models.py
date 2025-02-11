import random
import string
from pathlib import Path
from typing import ClassVar, Self

from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from digitaldome.common.models import TimestampedModel
from entities.helpers import format_time_spent

### Near-constant models ###


class Tag(TimestampedModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self: Self) -> str:
        return self.name


class Platform(TimestampedModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self: Self) -> str:
        return self.name


### Dynamic models ###


class EntityQueryset(models.QuerySet):
    pass


def image_upload_destination(instance: models.Model, filename: str) -> str:
    ext = Path(filename).suffix
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=14))  # noqa: S311
    return f"entities/{instance.__class__.__name__.lower()}s/{random_string}{ext}"


class EntityBase(TimestampedModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, validators=[MaxLengthValidator(500)])

    image = models.ImageField(upload_to=image_upload_destination, blank=True)

    wikipedia_url = models.URLField(verbose_name=_("Wikipedia URL"), blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    # Fields and their icon's partial templates (svg as HTML file)
    # that are show in the detail view.
    ADDITIONAL_LINK_AS_ICON_FIELDS: tuple[tuple[str, str]] = (
        ("wikipedia_url", "entities/partials/icons/wikipedia_svg.html"),
    )

    # Fields that are shown in the detail view.
    # Their HTML representation can be configured with a function named
    # `get_<field_name>_display` on the model.
    ADDITIONAL_DETAIL_FIELDS: tuple[str] = ()

    objects = EntityQueryset.as_manager()

    # Used in the frontend to color the entity type record
    COLOR: str

    class Meta:
        abstract = True
        constraints: ClassVar = [
            models.UniqueConstraint(
                Lower("name"),
                name="%(class)s_unique_name",
                violation_error_message=_("Item with that name already exists."),
            ),
        ]
        indexes: ClassVar = [
            GinIndex(
                fields=["name"],
                name="%(class)s_trgm_name_idx",
                opclasses=["gin_trgm_ops"],
            ),
        ]
        ordering = ("name", "-id")

    def get_absolute_url(self: Self) -> str:
        return reverse("entities:entities-detail", kwargs={"entity_type": self._meta.verbose_name, "pk": self.pk})


class Movie(EntityBase):
    release_date = models.DateField(null=True, blank=True)

    imdb_url = models.URLField(verbose_name=_("IMDB URL"), blank=True)

    length = models.PositiveSmallIntegerField(null=True, blank=True)  # In minutes

    director = ArrayField(models.CharField(max_length=255), default=list, blank=True)
    cast = ArrayField(models.CharField(max_length=255), default=list, blank=True)

    ADDITIONAL_LINK_AS_ICON_FIELDS = (
        *EntityBase.ADDITIONAL_LINK_AS_ICON_FIELDS,
        ("imdb_url", "entities/partials/icons/imdb_svg.html"),
    )

    ADDITIONAL_DETAIL_FIELDS = ("release_date", "length", "director", "cast")

    COLOR = "#f44336"

    def __str__(self: Self) -> str:
        res = self.name
        if self.release_date:
            res += f" ({self.release_date.year})"

        return res

    def get_length_display(self: Self) -> str:
        if not self.length:
            return ""

        return format_time_spent(self.length)


class Show(EntityBase):
    release_date = models.DateField(null=True, blank=True)

    imdb_url = models.URLField(verbose_name=_("IMDB URL"), blank=True)

    creator = ArrayField(models.CharField(max_length=255), default=list, blank=True)
    stars = ArrayField(models.CharField(max_length=255), default=list, blank=True)

    ADDITIONAL_LINK_AS_ICON_FIELDS = (
        *EntityBase.ADDITIONAL_LINK_AS_ICON_FIELDS,
        ("imdb_url", "entities/partials/icons/imdb_svg.html"),
    )

    ADDITIONAL_DETAIL_FIELDS = ("release_date", "creator", "stars")

    COLOR = "#ff9800"

    def __str__(self: Self) -> str:
        return self.name


class Game(EntityBase):
    release_date = models.DateField(null=True, blank=True)

    steam_url = models.URLField(verbose_name=_("Steam URL"), blank=True)

    platforms = models.ManyToManyField(Platform, blank=True)

    developer = ArrayField(models.CharField(max_length=255), default=list, blank=True)
    publisher = ArrayField(models.CharField(max_length=255), default=list, blank=True)

    ADDITIONAL_LINK_AS_ICON_FIELDS = (
        *EntityBase.ADDITIONAL_LINK_AS_ICON_FIELDS,
        ("steam_url", "entities/partials/icons/steam_svg.html"),
    )

    ADDITIONAL_DETAIL_FIELDS = ("release_date", "platforms", "developer", "publisher")

    COLOR = "#4caf50"

    def __str__(self: Self) -> str:
        return self.name


class Book(EntityBase):
    publish_date = models.DateField(null=True, blank=True)

    goodreads_url = models.URLField(verbose_name=_("Goodreads URL"), blank=True)

    author = ArrayField(models.CharField(max_length=255), default=list, blank=True)

    ADDITIONAL_LINK_AS_ICON_FIELDS = (
        *EntityBase.ADDITIONAL_LINK_AS_ICON_FIELDS,
        ("goodreads_url", "entities/partials/icons/goodreads_svg.html"),
    )

    ADDITIONAL_DETAIL_FIELDS = ("publish_date", "author")

    COLOR = "#2196f3"

    def __str__(self: Self) -> str:
        return self.name
