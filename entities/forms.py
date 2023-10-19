from typing import Any, ClassVar, Self

from django import forms

from digitaldome.common.fields import GetOrCreateManyToManyField
from digitaldome.common.widgets import ArrayField, ClearableFileInputWithImagePreview
from entities.models import Book, EntityBase, Game, Identity, Movie, Show, Tag


class EntityBaseForm(forms.ModelForm):
    tags = GetOrCreateManyToManyField(queryset=Tag.objects.all(), to_field_name="name", required=False)

    class Meta:
        fields = ("name", "description", "image", "tags")
        widgets: ClassVar = {
            "image": ClearableFileInputWithImagePreview(),
        }

    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def _check_if_all_required_fields_filled(self: Self) -> None:
        return all(self.cleaned_data.get(field) for field in self.instance.ADDITIONAL_DETAIL_FIELDS)

    def save(self: Self, commit: bool = True) -> EntityBase:
        self.instance.created_by = self.user
        self.instance.draft = not self._check_if_all_required_fields_filled()
        return super().save(commit)


class IdentityForm(EntityBaseForm):
    class Meta(EntityBaseForm.Meta):
        model = Identity
        fields = (*EntityBaseForm.Meta.fields, *("birth_date",))
        widgets: ClassVar = {
            **EntityBaseForm.Meta.widgets,
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }


class MovieForm(EntityBaseForm):
    director = GetOrCreateManyToManyField(queryset=Identity.objects.all(), to_field_name="name", required=False)
    cast = GetOrCreateManyToManyField(queryset=Identity.objects.all(), to_field_name="name", required=False)

    class Meta(EntityBaseForm.Meta):
        model = Movie
        fields = (*EntityBaseForm.Meta.fields, *("release_date", "length", "director", "cast"))
        widgets: ClassVar = {
            **EntityBaseForm.Meta.widgets,
            "release_date": forms.DateInput(attrs={"type": "date"}),
        }


class ShowForm(EntityBaseForm):
    class Meta(EntityBaseForm.Meta):
        model = Show
        fields = (*EntityBaseForm.Meta.fields, *("release_date", "creator", "stars"))
        widgets: ClassVar = {
            **EntityBaseForm.Meta.widgets,
            "release_date": forms.DateInput(attrs={"type": "date"}),
        }


class GameForm(EntityBaseForm):
    producer = GetOrCreateManyToManyField(queryset=Identity.objects.all(), to_field_name="name", required=False)
    publisher = GetOrCreateManyToManyField(queryset=Identity.objects.all(), to_field_name="name", required=False)

    class Meta(EntityBaseForm.Meta):
        model = Game
        fields = (
            *EntityBaseForm.Meta.fields,
            *("release_date", "platforms", "producer", "publisher"),
        )
        widgets: ClassVar = {
            **EntityBaseForm.Meta.widgets,
            "release_date": forms.DateInput(attrs={"type": "date"}),
            "platforms": ArrayField(),
        }


class BookForm(EntityBaseForm):
    author = GetOrCreateManyToManyField(queryset=Identity.objects.all(), to_field_name="name", required=False)

    class Meta(EntityBaseForm.Meta):
        model = Book
        fields = (*EntityBaseForm.Meta.fields, *("publish_date", "author"))
        widgets: ClassVar = {
            **EntityBaseForm.Meta.widgets,
            "publish_date": forms.DateInput(attrs={"type": "date"}),
        }
