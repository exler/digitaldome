from typing import ClassVar, Self

from django import forms
from django.templatetags.static import static

from digitaldome.common.widgets import ClearableFileInputWithImagePreview
from digitaldome.utils.image import resize_and_crop_image
from users.models import User


class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("avatar", "bio")
        widgets: ClassVar = {
            "avatar": ClearableFileInputWithImagePreview(
                attrs={"width": 80, "height": 80, "placeholder": static("img/avatar-placeholder.png")}
            ),
        }

    def clean_avatar(self: Self) -> None:
        if avatar := self.cleaned_data.get("avatar"):
            avatar = resize_and_crop_image(avatar, User.AVATAR_WIDTH, User.AVATAR_HEIGHT)
        return avatar
