from typing import Any, ClassVar, Self

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.validators import RegexValidator
from django.db import models
from django.templatetags.static import static
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class CustomUserQuerySet(models.QuerySet):
    def active(self: Self) -> Self:
        return self.filter(is_active=True, email_verified=True)


class CustomUserManager(UserManager.from_queryset(CustomUserQuerySet)):
    def _create_user(self: Self, display_name: str, email: str, password: str, **extra_fields: Any) -> Any:
        """
        Create and save a User with the provided email and password.
        """
        if not email:
            raise ValueError("The given email address must be set")

        email = self.normalize_email(email)
        user = self.model(display_name=display_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self: Self, display_name: str, email: str, password: str, **extra_fields: Any) -> Any:
        return self._create_user(display_name, email, password, **extra_fields)

    def create_superuser(self: Self, display_name: str, email: str, password: str, **extra_fields: Any) -> Any:
        extra_fields.setdefault("is_moderator", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("email_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(display_name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Default user model.
    """

    display_name = models.CharField(
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Alphanumeric, spaces and ./-/_ characters only."),
        validators=[RegexValidator(r"^[\w. -]+\Z")],
        error_messages={
            "unique": _("A user with that display name already exists."),
        },
    )

    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True)

    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)

    is_moderator = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    AVATAR_WIDTH = 128
    AVATAR_HEIGHT = 128

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar = ["display_name"]

    def __str__(self: Self) -> str:
        return f"{self.display_name} ({self.email})"

    @cached_property
    def avatar_url(self: Self) -> str | None:
        """
        Gets avatar URL to display or a placeholder if user has no avatar.
        """
        if self.avatar:
            return self.avatar.url

        return static("img/avatar-placeholder.png")
