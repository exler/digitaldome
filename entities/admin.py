from typing import Self

from django.contrib import admin
from django.utils.safestring import mark_safe

from entities.models import Book, EntityBase, Game, Movie, Show


class EntityBaseAdmin(admin.ModelAdmin):
    list_display = ("__str__", "thumbnail", "draft", "approved")

    def thumbnail(self: Self, obj: EntityBase) -> str:
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='48' height='72' />")  # noqa: S308

        return "-"


@admin.register(Movie)
class MovieAdmin(EntityBaseAdmin):
    pass


@admin.register(Show)
class ShowAdmin(EntityBaseAdmin):
    pass


@admin.register(Game)
class GameAdmin(EntityBaseAdmin):
    pass


@admin.register(Book)
class BookAdmin(EntityBaseAdmin):
    pass
