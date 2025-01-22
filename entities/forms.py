from typing import Any, ClassVar, Self

from django import forms
from django.templatetags.static import static

from digitaldome.common.fields import GetOrCreateManyToManyField
from digitaldome.common.widgets import ArrayField, ClearableFileInputWithImagePreview, TimeWidget
from digitaldome.utils.image import resize_and_crop_image
from entities.models import Book, EntityBase, Game, Movie, Show, Tag


class EntityBaseForm(forms.ModelForm):
    tags = GetOrCreateManyToManyField(queryset=Tag.objects.all(), to_field_name="name", required=False)

    class Meta:
        fields = ("name", "description", "image", "wikipedia_url", "tags")
        widgets: ClassVar = {
            "image": ClearableFileInputWithImagePreview(
                attrs={"width": 96, "height": 144, "placeholder": static("img/image-placeholder.png")}
            ),
        }

    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_image(self: Self) -> None:
        if image := self.cleaned_data.get("image"):
            image = resize_and_crop_image(image, EntityBase.IMAGE_WIDTH, EntityBase.IMAGE_HEIGHT)
        return image

    def save(self: Self, commit: bool = True) -> EntityBase:
        self.instance.created_by = self.user
        return super().save(commit)


class MovieForm(EntityBaseForm):
    class Meta(EntityBaseForm.Meta):
        model = Movie
        fields = (*EntityBaseForm.Meta.fields, *("release_date", "length", "director", "cast", "imdb_url"))
        widgets: ClassVar = {
            **EntityBaseForm.Meta.widgets,
            "length": TimeWidget(attrs={"style": "width: inherit;"}),
            "director": ArrayField(),
            "cast": ArrayField(),
            "release_date": forms.DateInput(attrs={"type": "date"}),
        }


class ShowForm(EntityBaseForm):
    class Meta(EntityBaseForm.Meta):
        model = Show
        fields = (*EntityBaseForm.Meta.fields, *("release_date", "creator", "stars", "imdb_url"))
        widgets: ClassVar = {
            **EntityBaseForm.Meta.widgets,
            "release_date": forms.DateInput(attrs={"type": "date"}),
            "creator": ArrayField(),
            "stars": ArrayField(),
        }


class GameForm(EntityBaseForm):
    class Meta(EntityBaseForm.Meta):
        model = Game
        fields = (
            *EntityBaseForm.Meta.fields,
            *("release_date", "platforms", "developer", "publisher", "steam_url"),
        )
        widgets: ClassVar = {
            **EntityBaseForm.Meta.widgets,
            "release_date": forms.DateInput(attrs={"type": "date"}),
            "developer": ArrayField(),
            "publisher": ArrayField(),
            "platforms": ArrayField(),
        }


class BookForm(EntityBaseForm):
    class Meta(EntityBaseForm.Meta):
        model = Book
        fields = (*EntityBaseForm.Meta.fields, *("publish_date", "author", "goodreads_url"))
        widgets: ClassVar = {
            **EntityBaseForm.Meta.widgets,
            "author": ArrayField(),
            "publish_date": forms.DateInput(attrs={"type": "date"}),
        }
