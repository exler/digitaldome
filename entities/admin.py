from django.contrib import admin

from entities.models import Book, Game, Movie, Show


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    pass


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass
