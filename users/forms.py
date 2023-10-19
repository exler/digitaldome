from typing import Any, ClassVar, Self

from django import forms
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import Http404, HttpRequest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from digitaldome.utils.url import get_full_url
from users.tokens import EmailVerificationTokenGenerator, PasswordResetTokenGenerator

from .models import User


class LoginForm(forms.ModelForm):
    error_messages: ClassVar = {
        "invalid_credentials": _(
            "Please enter a correct email and password. Note that both fields may be case-sensitive."
        ),
        "user_inactive": _("This account is inactive."),
    }

    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("email", "password", "remember_me")
        widgets: ClassVar = {"password": forms.PasswordInput()}

    def __init__(self: Self, request: HttpRequest | None = None, *args: Any, **kwargs: Any) -> None:
        self.request = request
        self.user_cache: User | None = None

        super().__init__(*args, **kwargs)

    def clean(self: Self) -> dict[str, Any]:
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
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


class RegisterForm(forms.ModelForm):
    error_messages: ClassVar = {
        "password_mismatch": _("The two password fields didn't match."),
    }

    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("email", "display_name", "password", "confirm_password")
        widgets: ClassVar = {"password": forms.PasswordInput()}

    def clean_confirm_password(self: Self) -> None:
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )

    def send_email_verification_email(self: Self, user: User) -> None:
        email_verification_token = EmailVerificationTokenGenerator.make_token(obj=user)
        reset_url = get_full_url(reverse("users:verify-email", kwargs={"token": email_verification_token}))
        send_mail(
            subject="Verify your email",
            message=f"Click here to verify your email: {reset_url}",
            from_email=None,
            recipient_list=[user.email],
        )

    def save(self: Self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        self.send_email_verification_email(user)
        return user


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def send_password_reset_email(self: Self, user: User) -> None:
        password_reset_token = PasswordResetTokenGenerator.make_token(obj=user)
        reset_url = get_full_url(reverse("users:reset-password-confirm", kwargs={"token": password_reset_token}))

        send_mail(
            subject="Reset your password",
            message=f"Click here to reset your password: {reset_url}",
            from_email=None,
            recipient_list=[user.email],
        )

    def get_user_from_email(self: Self, email: str) -> User:
        """
        Given an email, return matching user who should receive a reset.
        """
        try:
            user = User.objects.get(email__iexact=email, is_active=True, email_verified=True)
        except User.DoesNotExist:
            raise Http404

        return user

    def save(self: Self) -> None:
        """
        Generate a one-use only link for resetting password and send it to the user.
        """
        email = self.cleaned_data["email"]
        user = self.get_user_from_email(email)
        self.send_password_reset_email(user)


class ResetPasswordConfirmForm(forms.Form):
    error_messages: ClassVar = {
        "password_mismatch": _("The two password fields didn't match."),
    }

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self: Self, user: User, *args: Any, **kwargs: Any) -> None:
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self: Self) -> None:
        password = self.cleaned_data.get("password")
        password_validation.validate_password(password, self.user)
        return password

    def clean_confirm_password(self: Self) -> None:
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )

    def save(self: Self, commit: bool = True, *args: Any, **kwargs: Any) -> None:
        password = self.cleaned_data["password"]
        self.user.set_password(password)
        if commit:
            self.user.save(update_fields=["password"])
        return self.user
