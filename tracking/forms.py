from typing import Any, Self

from django import forms

from tracking.models import TrackingObject


class TrackingObjectForm(forms.ModelForm):
    class Meta:
        model = TrackingObject
        fields = ["status"]

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
