import datetime
from typing import ClassVar, Self

from django.contrib import admin, messages
from django.core.files import File
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import path
from django.urls.resolvers import URLPattern
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from entities.helpers import make_imdb_url
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
from integrations.external.igdb import igdb_client
from integrations.external.tmdb import TMDBSupportedEntityType, tmdb_client


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
    prepopulated_fields: ClassVar = {"slug": ("name",)}

    actions = ("fill_automagically_action",)

    def redirect_to_change_view(self: Self, object_id: int) -> HttpResponse:
        """
        Redirect to change view (details) of the entity.
        """

        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return redirect(f"admin:{app_label}_{model_name}_change", object_id)

    def thumbnail(self: Self, obj: EntityBase) -> str:
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='80' height='120' />")  # noqa: S308

        return "-"

    def get_urls(self: Self) -> list[URLPattern]:
        default_urls = super().get_urls()

        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        custom_urls = [
            path(
                "<path:object_id>/fill-automagically/",
                self.admin_site.admin_view(self.fill_automagically_view),
                name=f"fill-automagically-{app_label}-{model_name}",
            )
        ]
        return custom_urls + default_urls

    def _fill_automagically(self: Self, request: HttpRequest, object_id: int) -> None:
        """
        Fill entity data using entity-specific approach (usually external API call).

        Save the entity after filling the data.
        """
        raise NotImplementedError

    @admin.action(description="Fill automagically", permissions=["change"])
    def fill_automagically_action(self, request: HttpRequest, queryset: QuerySet[EntityBase]) -> None:
        try:
            for entity in queryset:
                self._fill_automagically(request=request, object_id=entity.id)
        except NotImplementedError:
            messages.add_message(request, messages.WARNING, "Cannot fill automagically for this entity type.")
        else:
            messages.add_message(
                request, messages.SUCCESS, f"Data filled automagically for {queryset.count()} entities."
            )

    def fill_automagically_view(self: Self, request: HttpRequest, object_id: int) -> HttpResponse:
        try:
            self._fill_automagically(request=request, object_id=object_id)
        except NotImplementedError:
            messages.add_message(request, messages.WARNING, "Cannot fill automagically for this entity type.")
        else:
            messages.add_message(request, messages.SUCCESS, "Entity data filled automagically.")

        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return redirect(f"admin:{app_label}_{model_name}_change", object_id)


@admin.register(Movie)
class MovieAdmin(EntityBaseAdmin):
    def _fill_automagically(self, request: HttpRequest, object_id: int) -> None:
        movie_entity_obj = Movie.objects.get(id=object_id)

        response = tmdb_client.search(TMDBSupportedEntityType.MOVIE, movie_entity_obj.name)
        if len(response["results"]) < 1:
            messages.add_message(request, messages.ERROR, "No data found for this movie.")
            return

        movie_id = response["results"][0]["id"]
        movie_details = tmdb_client.get_details(TMDBSupportedEntityType.MOVIE, movie_id)

        if not movie_entity_obj.description:
            movie_entity_obj.description = movie_details["overview"]

        if not movie_entity_obj.length:
            movie_entity_obj.length = movie_details["runtime"]

        if not movie_entity_obj.release_date:
            movie_entity_obj.release_date = movie_details["release_date"]

        if not movie_entity_obj.tags.exists():
            tag_objs = []
            for genre in movie_details["genres"]:
                tag = MovieTag.objects.get_or_create_with_aliases(genre["name"])[0]
                tag_objs.append(tag)

            movie_entity_obj.tags.set(tag_objs)

        if not movie_entity_obj.imdb_url:
            movie_entity_obj.imdb_url = make_imdb_url(movie_details["imdb_id"])

        if not movie_entity_obj.image:
            image_path = movie_details["poster_path"]
            image_content = File(tmdb_client.get_image("w500", image_path))
            movie_entity_obj.image.save(image_path, image_content, save=False)

        movie_entity_obj.save()

        return self.redirect_to_change_view(object_id)


@admin.register(Show)
class ShowAdmin(EntityBaseAdmin):
    def _fill_automagically(self, request: HttpRequest, object_id: int) -> None:
        show_entity_obj = Show.objects.get(id=object_id)

        response = tmdb_client.search(TMDBSupportedEntityType.SHOW, show_entity_obj.name)
        if len(response["results"]) < 1:
            messages.add_message(request, messages.ERROR, "No data found for this show.")
            return

        show_id = response["results"][0]["id"]
        show_details = tmdb_client.get_details(TMDBSupportedEntityType.SHOW, show_id)

        if not show_entity_obj.description:
            show_entity_obj.description = show_details["overview"]

        if not show_entity_obj.release_date:
            show_entity_obj.release_date = show_details["first_air_date"]

        if not show_entity_obj.tags.exists():
            tag_objs = []
            for genre in show_details["genres"]:
                tag = ShowTag.objects.get_or_create(name=genre["name"])[0]
                tag_objs.append(tag)

            show_entity_obj.tags.set(tag_objs)

        if not show_entity_obj.image:
            image_path = show_details["poster_path"]
            image_content = File(tmdb_client.get_image("w500", image_path))
            show_entity_obj.image.save(image_path, image_content, save=False)

        show_entity_obj.save()

        return self.redirect_to_change_view(object_id)


@admin.register(Game)
class GameAdmin(EntityBaseAdmin):
    autocomplete_fields = (*EntityBaseAdmin.autocomplete_fields, *("platforms",))

    def _fill_automagically(self, request: HttpRequest, object_id: int) -> None:
        game_entity_obj = Game.objects.get(id=object_id)

        response = igdb_client.search(game_entity_obj.name)
        if len(response) < 1:
            messages.add_message(request, messages.ERROR, "No data found for this game.")
            return

        game_details = response[0]

        if not game_entity_obj.description:
            game_entity_obj.description = game_details["summary"]

        if not game_entity_obj.release_date:
            game_entity_obj.release_date = datetime.date.fromtimestamp(game_details["first_release_date"])

        if not game_entity_obj.tags.exists():
            tag_objs = []
            for genre in game_details["genres"]:
                tag = GameTag.objects.get_or_create_with_aliases(genre["name"])[0]
                tag_objs.append(tag)

            game_entity_obj.tags.set(tag_objs)

        if not game_entity_obj.platforms.exists():
            platform_objs = []
            for platform in game_details["platforms"]:
                try:
                    platform_obj = Platform.objects.get_with_aliases(platform["name"])
                    platform_objs.append(platform_obj)
                except Platform.DoesNotExist:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        f"Platform '{platform['name']}' not found. Please create it first.",
                    )

            game_entity_obj.platforms.set(platform_objs)

        if not game_entity_obj.developer:
            for company in game_details["involved_companies"]:
                if company["developer"]:
                    game_entity_obj.developer.append(company["company"]["name"])

        if not game_entity_obj.publisher:
            for company in game_details["involved_companies"]:
                if company["publisher"]:
                    game_entity_obj.publisher.append(company["company"]["name"])

        if not game_entity_obj.image:
            image_id = game_details["cover"]["image_id"]
            image_content = File(igdb_client.get_cover_image(image_id))
            game_entity_obj.image.save(f"{image_id}.webp", image_content, save=False)

        if not game_entity_obj.steam_url:
            for website in game_details.get("websites", []):
                if website["type"]["type"] == "Steam":
                    game_entity_obj.steam_url = website["url"]
                    break

        if not game_entity_obj.wikipedia_url:
            for website in game_details.get("websites", []):
                if website["type"]["type"] == "Wikipedia":
                    game_entity_obj.wikipedia_url = website["url"]
                    break

        game_entity_obj.save()

        return self.redirect_to_change_view(object_id)


@admin.register(Book)
class BookAdmin(EntityBaseAdmin):
    pass
