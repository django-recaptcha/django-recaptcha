from django.apps import AppConfig
from django.core.checks import register, Tags

from captcha.checks import recaptcha_key_check


class CaptchaConfig(AppConfig):
    name = "captcha"
    verbose_name = "Django reCAPTCHA"

    def ready(self):
        register(recaptcha_key_check, Tags.security)
