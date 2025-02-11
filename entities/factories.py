import factory

from entities.models import Book, Game, Movie, Show


class EntityFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    description = factory.Faker("text")

    wikipedia_url = factory.Faker("url")


class MovieFactory(EntityFactory):
    class Meta:
        model = Movie
        django_get_or_create = ("name",)


class ShowFactory(EntityFactory):
    class Meta:
        model = Show
        django_get_or_create = ("name",)


class GameFactory(EntityFactory):
    class Meta:
        model = Game
        django_get_or_create = ("name",)


class BookFactory(EntityFactory):
    class Meta:
        model = Book
        django_get_or_create = ("name",)
