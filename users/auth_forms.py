from typing import Any, ClassVar, Self

from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import User


class LoginForm(forms.ModelForm):
    error_messages: ClassVar = {
        "invalid_credentials": _(
            "Please enter a correct username and password. Note that both fields may be case-sensitive."
        ),
        "user_inactive": _("This account is inactive."),
    }

    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("username", "password", "remember_me")
        widgets: ClassVar = {"password": forms.PasswordInput()}

    def __init__(self: Self, request: HttpRequest | None = None, *args: Any, **kwargs: Any) -> None:
        self.request = request
        self.user_cache: User | None = None

        super().__init__(*args, **kwargs)

    def clean(self: Self) -> dict[str, Any]:
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                error = self.get_invalid_credentials_error()
                raise error
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def get_invalid_credentials_error(self: Self) -> ValidationError:
        return ValidationError(
            self.error_messages["invalid_credentials"],
            code="invalid_credentials",
        )

    def confirm_login_allowed(self: Self, user: User) -> None:
        if not user.is_active:
            raise ValidationError(self.error_messages["user_inactive"], code="user_inactive")

    def get_user(self: Self) -> User | None:
        return self.user_cache
