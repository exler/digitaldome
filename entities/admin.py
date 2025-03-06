from typing import Self

from django.contrib import admin, messages
from django.db.models import ManyToManyField
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import path
from django.urls.resolvers import URLPattern
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from entities.models import (
    Book,
    BookTag,
    EntityBase,
    Game,
    GameTag,
    Movie,
    MovieTag,
    Platform,
    Show,
    ShowTag,
)
from integrations.openai.client import get_openai_json_response
from integrations.openai.prompts import GET_ENTITY_PROMPT


class MovieInline(admin.TabularInline):
    model = Movie.tags.through
    extra = 0
    can_delete = False
    verbose_name = _("Movie with this tag")
    verbose_name_plural = _("Movies with this tag")

    def has_add_permission(self: Self, request: HttpRequest, obj: Movie) -> bool:
        return False

    def has_change_permission(self: Self, request: HttpRequest, obj: Movie | None = None) -> bool:
        return False


class ShowInline(admin.TabularInline):
    model = Show.tags.through
    extra = 0
    can_delete = False
    verbose_name = _("Show with this tag")
    verbose_name_plural = _("Shows with this tag")

    def has_add_permission(self: Self, request: HttpRequest, obj: Show) -> bool:
        return False

    def has_change_permission(self: Self, request: HttpRequest, obj: Show | None = None) -> bool:
        return False


class GameInline(admin.TabularInline):
    model = Game.tags.through
    extra = 0
    can_delete = False
    verbose_name = _("Game with this tag")
    verbose_name_plural = _("Games with this tag")

    def has_add_permission(self: Self, request: HttpRequest, obj: Game) -> bool:
        return False

    def has_change_permission(self: Self, request: HttpRequest, obj: Game | None = None) -> bool:
        return False


class BookInline(admin.TabularInline):
    model = Book.tags.through
    extra = 0
    can_delete = False
    verbose_name = _("Book with this tag")
    verbose_name_plural = _("Books with this tag")

    def has_add_permission(self: Self, request: HttpRequest, obj: Book) -> bool:
        return False

    def has_change_permission(self: Self, request: HttpRequest, obj: Book | None = None) -> bool:
        return False


class TagBaseAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(BookTag)
class BookTagAdmin(TagBaseAdmin):
    inlines = (BookInline,)


@admin.register(GameTag)
class GameTagAdmin(TagBaseAdmin):
    inlines = (GameInline,)


@admin.register(MovieTag)
class MovieTagAdmin(TagBaseAdmin):
    inlines = (MovieInline,)


@admin.register(ShowTag)
class ShowTagAdmin(TagBaseAdmin):
    inlines = (ShowInline,)


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class EntityBaseAdmin(admin.ModelAdmin):
    change_form_template = "entities/admin/change_form.html"

    list_display = ("__str__", "thumbnail")
    search_fields = ("name",)
    autocomplete_fields = ("tags",)

    def thumbnail(self: Self, obj: EntityBase) -> str:
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='48' height='72' />")  # noqa: S308

        return "-"

    def get_urls(self: Self) -> list[URLPattern]:
        default_urls = super().get_urls()

        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        custom_urls = [
            path(
                "<path:object_id>/fill-automagically/",
                self.admin_site.admin_view(self.fill_automagically),
                name=f"fill-automagically-{app_label}-{model_name}",
            )
        ]
        return custom_urls + default_urls

    def fill_automagically(self: Self, request: HttpRequest, object_id: int) -> HttpResponse:
        entity: EntityBase = self.model.objects.get(id=object_id)

        response = get_openai_json_response(
            system_prompt=GET_ENTITY_PROMPT, user_prompt=f"{entity._meta.verbose_name} | {entity.name}"
        )

        for key, value in response.items():
            field = self.model._meta.get_field(key)
            if isinstance(field, ManyToManyField):
                target_model = field.related_model
                target_model.objects.bulk_create(
                    [target_model(name=v) for v in value],
                    ignore_conflicts=True,
                )
                getattr(entity, key).set(target_model.objects.filter(name__in=value))
            else:
                setattr(entity, key, value)

        entity.save()

        messages.add_message(request, messages.SUCCESS, "Entity data filled automagically.")

        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name

        return redirect(f"admin:{app_label}_{model_name}_change", object_id)


@admin.register(Movie)
class MovieAdmin(EntityBaseAdmin):
    pass


@admin.register(Show)
class ShowAdmin(EntityBaseAdmin):
    pass


@admin.register(Game)
class GameAdmin(EntityBaseAdmin):
    autocomplete_fields = (*EntityBaseAdmin.autocomplete_fields, *("platforms",))


@admin.register(Book)
class BookAdmin(EntityBaseAdmin):
    pass
