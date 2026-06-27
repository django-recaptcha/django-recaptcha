import os
from pathlib import Path

sandbox = Path(__file__).resolve().parent


INSTALLED_APPS = [
    "django_recaptcha",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

SECRET_KEY = "not a safe key for production"

DEBUG = True

SILENCED_SYSTEM_CHECKS = ["django_recaptcha.recaptcha_test_key_error"]

ROOT_URLCONF = "sandbox.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            sandbox / "templates",
        ],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
