from django.core.exceptions import ValidationError


class CaptchaHostnameError(ValidationError):
    pass
