
from django.core.exceptions import ValidationError

class CaptchaHTTPError(ValidationError):
    pass


class CaptchaValidationError(ValidationError):
    pass


class CaptchaHostnameError(ValidationError):
    pass


class CaptchaScoreError(ValidationError):
    pass

