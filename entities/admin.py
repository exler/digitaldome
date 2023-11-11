from typing import Self

from django.contrib import admin, messages
from django.db.models import ManyToManyField
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import path
from django.urls.resolvers import URLPattern
from django.utils.safestring import mark_safe

from entities.models import Book, EntityBase, Game, Movie, Show
from integrations.openai.client import get_openai_json_response
from integrations.openai.prompts import GET_ENTITY_PROMPT


class EntityBaseAdmin(admin.ModelAdmin):
    change_form_template = "entities/admin/change_form.html"

    list_display = ("__str__", "thumbnail", "draft", "approved")
    search_fields = ("name",)

    def thumbnail(self: Self, obj: EntityBase) -> str:
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='48' height='72' />")  # noqa: S308

        return "-"

    def get_urls(self: Self) -> list[URLPattern]:
        default_urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/fill-automagically/",
                self.admin_site.admin_view(self.fill_automagically),
                name="fill-automagically",
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
    pass


@admin.register(Book)
class BookAdmin(EntityBaseAdmin):
    pass
