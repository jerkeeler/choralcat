"""
Django settings for choralcat project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

import environ
import sentry_sdk
from django.core.management.utils import get_random_secret_key
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env(
    ADMIN_NAMES=(list[str], []),
    ADMIN_EMAILS=(list[str], []),
    ALLOWED_HOSTS=(list[str], ["localhost"]),
    DEBUG=(bool, False),
    EMAIL_HOST=(str, None),
    EMAIL_HOST_PASSWORD=(str, None),
    EMAIL_HOST_USER=(str, None),
    EMAIL_PORT=(str, None),
    ERROR_LOG_LOCATION=(str, os.path.join("data", "logs", "error.log")),
    INTERNAL_IPS=(list[str], ["127.0.0.1"]),
    LOG_LEVEL=(str, "INFO"),
    LOG_LOCATION=(str, os.path.join("data", "logs", "application.log")),
    REDIS_HOST=(str, "127.0.0.1"),
    REDIS_PORT=(str, "6379"),
    SECRET_KEY=(str, get_random_secret_key()),
    SENTRY_DSN=(str, None),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")
INTERNAL_IPS = env("INTERNAL_IPS")

APP_VERSION = None
app_version_path = os.path.join(BASE_DIR, ".version")
if os.path.exists(app_version_path):
    APP_VERSION = open(app_version_path).read().strip()

SENTRY_DSN = env("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        sample_rate=1.0,  # Capture all errors
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.05,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
        release=APP_VERSION,
        environment="development" if DEBUG else "production",
    )

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "django_celery_results",
    "django_celery_beat",
    # "defender",
    "debug_toolbar",
    "choralcat.core.apps.ChoralcatCoreConfig",
    "choralcat.data_migrations.apps.DataMigrationsConfig",
    "choralcat.web.apps.ChoralcatWebConfig",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "defender.middleware.FailedLoginMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "choralcat.core.middleware.TimezoneMiddleware",
]

ROOT_URLCONF = "choralcat.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "choralcat.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "data", "db.sqlite3"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/catalog"
LOGOUT_REDIRECT_URL = "/"

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# EMAIL CONFIG
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

# Disabling admin emails/names in favor of sentry integration
#     ADMIN_NAMES = env("ADMIN_NAMES")
#     ADMIN_EMAILS = env("ADMIN_EMAILS")
#     ADMINS = list(zip(ADMIN_NAMES, ADMIN_EMAILS))

# CELERY CONFIG
REDIS_HOST = env("REDIS_HOST")
REDIS_PORT = env("REDIS_PORT")
REDIS_PASSWORD = env("REDIS_PASSWORD")

CELERY_BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
CELERY_RESULT_BACKEND = "django-db"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

LOG_LEVEL = env("LOG_LEVEL")
LOG_LOCATION = env("LOG_LOCATION")
ERROR_LOG_LOCATION = env("ERROR_LOG_LOCATION")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {process:d} {thread:d} - {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {name} - {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "formatter": "simple",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "formatter": "verbose",
            "filters": ["require_debug_false"],
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "W6",
            "utc": True,
            "filename": LOG_LOCATION,
            "backupCount": 4,
        },
        "file_error": {
            "level": "ERROR",
            "formatter": "verbose",
            "filters": ["require_debug_false"],
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "W6",
            "utc": True,
            "filename": ERROR_LOG_LOCATION,
            "backupCount": 4,
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["file_error"],
            "level": "ERROR",
        },
        "choralcat": {
            "handlers": ["console", "file", "file_error"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
    },
}
