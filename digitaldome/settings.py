from pathlib import Path

import sentry_sdk
from botocore.config import Config as BotoConfig
from django.urls import reverse_lazy
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration

from digitaldome.utils.env import get_env_bool, get_env_float, get_env_list, get_env_str

load_dotenv()

# Base settings #

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_env_str("DJANGO_SECRET_KEY")

DEBUG = get_env_bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = get_env_list("DJANGO_ALLOWED_HOSTS")

CSRF_TRUSTED_ORIGINS = get_env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

BASE_URL = get_env_str("BASE_URL")

# Application definition #

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "digitaldome",
    "users",
    "entities",
    "tracking",
    "integrations",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "digitaldome.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "digitaldome.context_processors.base_url_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "digitaldome.wsgi.application"

# Sentry #
# https://docs.sentry.io/platforms/python/integrations/django/

if SENTRY_DSN := get_env_str("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=get_env_float("SENTRY_TRACES_SAMPLE_RATE", 0.0),
        send_default_pii=True,
    )

# Logging #
# https://docs.djangoproject.com/en/4.2/howto/logging/

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console"],
    },
    "formatters": {
        "verbose": {
            "()": "digitaldome.formatters.ExtraFormatter",
            "format": "[{asctime}] [{levelname}] [{name}] [{module}] {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        }
    },
}

# Database #
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_env_str("POSTGRES_DB_NAME"),
        "USER": get_env_str("POSTGRES_DB_USER"),
        "PASSWORD": get_env_str("POSTGRES_DB_PASSWORD"),
        "HOST": get_env_str("POSTGRES_DB_HOST"),
        "PORT": get_env_str("POSTGRES_DB_PORT", "5432"),
    }
}

# Cache #
# https://docs.djangoproject.com/en/4.2/topics/cache/

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "mechanical-sequence-version",
    }
}


# Authentication #

AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_URL = reverse_lazy("users:login")


# Internationalization #
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Storage and static files (CSS, JavaScript, Images) #
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": get_env_str("AWS_STORAGE_BUCKET_NAME"),
            "endpoint_url": get_env_str("AWS_S3_ENDPOINT_URL"),
            "access_key": get_env_str("AWS_S3_ACCESS_KEY"),
            "secret_key": get_env_str("AWS_S3_SECRET_KEY"),
            "region_name": get_env_str("AWS_S3_REGION_NAME"),
            "client_config": BotoConfig(
                request_checksum_calculation="when_required",
                response_checksum_validation="when_required",
            ),
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type #
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email #
# https://docs.djangoproject.com/en/4.2/ref/settings/#email-backend

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = get_env_str("EMAIL_HOST")
EMAIL_PORT = get_env_str("EMAIL_PORT")
EMAIL_HOST_USER = get_env_str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_env_str("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = get_env_bool("EMAIL_USE_TLS")
EMAIL_USE_SSL = get_env_bool("EMAIL_USE_SSL")
DEFAULT_FROM_EMAIL = get_env_str("DEFAULT_FROM_EMAIL")

# Integrations #
# TMDB API #
# https://developer.themoviedb.org/reference

TMDB_API_KEY = get_env_str("TMDB_API_KEY")
