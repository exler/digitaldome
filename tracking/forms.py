from typing import Any, ClassVar, Self

from django import forms

from tracking.models import TrackingObject


class DynamicFieldFormMixin:
    """
    This mixin makes the form only update the fields that are available
    in the supplied data.
    """

    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        fields_copy = self.fields.copy()
        for field in self.fields:
            if field not in self.data.keys():
                del fields_copy[field]

        self.fields = fields_copy


class TrackingObjectForm(DynamicFieldFormMixin, forms.ModelForm):
    class Meta:
        model = TrackingObject
        fields: ClassVar = ["status", "rating", "notes"]

    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        self.entity = kwargs.pop("entity", None)
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def save(self: Self, commit: bool = True) -> TrackingObject:
        instance = super().save(commit=False)
        instance.user = self.user
        instance.content_object = self.entity
        if commit:
            instance.save()
        return instance
