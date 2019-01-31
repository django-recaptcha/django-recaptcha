DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test.sqlite",
    }
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "captcha",
    "captcha.tests"
]

RECAPTCHA_PRIVATE_KEY = "privkey"
RECAPTCHA_PUBLIC_KEY = "pubkey"

SECRET_KEY = "SECRET_KEY"
