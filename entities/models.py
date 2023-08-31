from typing import Self

from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q

from digitaldome.common.models import TimestampedModel


class Genre(models.Model):
    name = models.CharField(max_length=255)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="genres",
        limit_choices_to=Q(app_label="entities") & ~Q(model="genre"),
    )

    def __str__(self: Self) -> str:
        return f"{self.name} ({self.content_type.model_class().__name__})"


class EntityBase(TimestampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    genres = models.ManyToManyField(Genre, related_name="+")

    release_date = models.DateField()

    class Meta:
        abstract = True


def cover_upload_target(instance: EntityBase, filename: str) -> str:
    return f"{instance.__class__.__name__.lower()}s/covers/{filename}"


class CoverModelMixin(models.Model):
    cover = models.ImageField(upload_to=cover_upload_target, null=True, blank=True)

    class Meta:
        abstract = True


class Movie(CoverModelMixin, EntityBase):
    length = models.PositiveSmallIntegerField()  # In minutes

    director = ArrayField(models.CharField(max_length=255))
    cast = ArrayField(models.CharField(max_length=255))

    def __str__(self: Self) -> str:
        return f"{self.name} ({self.release_date.year})"


class Show(EntityBase):
    def __str__(self: Self) -> str:
        return self.name


class Episode(EntityBase):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="episodes")

    season = models.PositiveSmallIntegerField()
    number = models.PositiveSmallIntegerField()

    def __str__(self: Self) -> str:
        return f"{self.show.name} S{self.season:02}E{self.number:02}"


class Game(CoverModelMixin, EntityBase):
    class Platforms(models.IntegerChoices):
        PC = 10, "PC"
        PS3 = 20, "PS3"
        PS4 = 21, "PS4"
        PS5 = 22, "PS5"
        XBOX_360 = 30, "Xbox 360"
        XBOX_ONE = 31, "Xbox One"
        SWITCH = 40, "Nintendo Switch"

    platforms = ArrayField(models.PositiveSmallIntegerField(choices=Platforms.choices))

    def __str__(self: Self) -> str:
        return self.name


class Book(CoverModelMixin, EntityBase):
    authors = ArrayField(models.CharField(max_length=255))

    pages = models.PositiveSmallIntegerField()

    isbn = models.CharField(max_length=17)

    def __str__(self: Self) -> str:
        return self.name
