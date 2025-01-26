from typing import Any, Self

from django.apps import apps
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.validators import RegexValidator
from django.db import models
from django.templatetags.static import static
from django.utils.deconstruct import deconstructible
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class CustomUserQuerySet(models.QuerySet):
    def active(self: Self) -> Self:
        return self.filter(is_active=True)


class CustomUserManager(UserManager.from_queryset(CustomUserQuerySet)):
    def _create_user(self: Self, username: str, password: str, **extra_fields: Any) -> Any:
        """
        Create and save a User with the provided username and password.
        """
        if not username:
            raise ValueError("The given username address must be set")

        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self: Self, username: str, password: str, **extra_fields: Any) -> Any:
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self: Self, username: str, password: str, **extra_fields: Any) -> Any:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


@deconstructible
class UsernameValidator(RegexValidator):
    regex = r"^[\w-]+$"
    message = _("Username can only contain letters, numbers, underscores, or hyphens.")
    code = "invalid_username"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(self.regex, self.message, self.code, *args, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Default user model.
    """

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and -/_ only."),
        validators=[UsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    AVATAR_WIDTH = 128
    AVATAR_HEIGHT = 128

    USERNAME_FIELD = "username"

    def __str__(self: Self) -> str:
        return self.username

    @cached_property
    def avatar_url(self: Self) -> str | None:
        """
        Gets avatar URL to display or a placeholder if user has no avatar.
        """
        if self.avatar:
            return self.avatar.url

        return static("img/avatar-placeholder.png")
