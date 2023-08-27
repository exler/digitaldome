from typing import Self

from django.contrib.postgres.fields import ArrayField
from django.db import models

from digitaldome.common.models import TimestampedModel


class EntityBase(TimestampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True


class Movie(EntityBase):
    class Genres(models.IntegerChoices):
        Action = 1
        Adventure = 2
        Animation = 3
        Comedy = 4
        Crime = 5
        Documentary = 6
        Drama = 7
        Family = 8
        Fantasy = 9
        Foreign = 10
        History = 11
        Horror = 12
        Music = 13
        Mystery = 14
        Romance = 15
        ScienceFiction = 16
        Thriller = 17
        War = 18
        Western = 19

    genres = ArrayField(models.IntegerField(choices=Genres.choices))

    year = models.IntegerField()

    poster = models.ImageField(upload_to="movies/posters", null=True, blank=True)

    def __str__(self: Self) -> str:
        return f"{self.name} ({self.year})"


class Show(EntityBase):
    class Genres(models.IntegerChoices):
        Action = 1
        Adventure = 2
        Animation = 3
        Children = 4
        Comedy = 5
        Crime = 6
        Documentary = 7
        Drama = 8
        Family = 9
        Fantasy = 10
        Food = 11
        GameShow = 12
        History = 13
        HomeAndGarden = 14
        Horror = 15
        KoreanDrama = 16
        MartialArts = 17
        MiniSeries = 18
        Musical = 19
        Mystery = 20
        Reality = 21
        Romance = 22
        ScienceFiction = 23
        Soap = 24
        Sport = 25
        Suspense = 26
        TalkShow = 27
        Thriller = 28
        Travel = 29
        War = 30
        Western = 31

    genres = ArrayField(models.IntegerField(choices=Genres.choices))

    poster = models.ImageField(upload_to="shows/posters", null=True, blank=True)

    def __str__(self: Self) -> str:
        return self.name


class Episode(EntityBase):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="episodes")

    season = models.PositiveSmallIntegerField()
    number = models.PositiveSmallIntegerField()

    release_date = models.DateField()

    def __str__(self: Self) -> str:
        return f"{self.show.name} S{self.season:02}E{self.number:02}"


class Game(EntityBase):
    release_date = models.DateField()

    cover = models.ImageField(upload_to="games/covers", null=True, blank=True)

    def __str__(self: Self) -> str:
        return self.name


class Book(EntityBase):
    class Genres(models.IntegerChoices):
        Art = 1
        Biography = 2
        Business = 3
        ChickLit = 4
        Children = 5
        Classics = 6
        Comics = 7
        Contemporary = 8
        Crime = 9
        Fantasy = 10
        Fiction = 11
        HistoricalFiction = 12
        History = 13
        Horror = 14
        HumorAndComedy = 15
        Manga = 16
        Music = 17
        Mystery = 18
        Nonfiction = 19
        Paranormal = 20
        Philosophy = 21
        Poetry = 22
        Psychology = 23
        Religion = 24
        Romance = 25
        Science = 26
        ScienceFiction = 27
        SelfHelp = 28
        Suspense = 29
        Spirituality = 30
        Sports = 31
        Thriller = 32
        Travel = 33
        YoungAdult = 34

    genres = ArrayField(models.IntegerField(choices=Genres.choices))

    cover = models.ImageField(upload_to="books/covers", null=True, blank=True)

    authors = ArrayField(models.CharField(max_length=255))

    published_date = models.DateField()

    def __str__(self: Self) -> str:
        return self.name
