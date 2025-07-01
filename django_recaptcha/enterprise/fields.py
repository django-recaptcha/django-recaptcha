from string import ascii_letters, digits
from typing import Any, Optional

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.forms.fields import Field
from django.http import HttpRequest

from .client import verify_enterprise_v1_token
from .conf import use_setting
from .widgets import ReCAPTCHAEnterpriseV1CheckboxWidget

# can only contain alphanumeric characters, slashes, and underscores
ACTION_ALLOWED_CHARS = set(ascii_letters + digits + "/" + "_")


def _action_name_is_valid(action: str) -> bool:
    """Checks whether name of a given action is valid.

    More information: https://cloud.google.com/recaptcha/docs/actions-website

    :param action: name of action
    """
    return all((ch in ACTION_ALLOWED_CHARS) for ch in action)


class ReCAPTCHAEnterpriseV1CheckboxField(Field):
    """Field that handles reCAPTCHA Enterprise V1 Checkbox tokens."""

    widget = ReCAPTCHAEnterpriseV1CheckboxWidget

    def __init__(
        self,
        *,
        project_id: Optional[str] = None,
        sitekey: Optional[str] = None,
        access_token: Optional[str] = None,
        action: Optional[str] = None,
        required_score: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
        """
        :param project_id: ID of Google cloud project associated with sitekey
        :param sitekey: public key used to integrate reCAPTCHA
        :param access_token: token used for authentication
        :param action: action associated with this reCAPTCHA field
        :param required_score: minimum score needed to pass validation
        """
        _project_id = use_setting("RECAPTCHA_ENTERPRISE_PROJECT_ID", project_id)
        if _project_id is None:
            raise ImproperlyConfigured(
                "Must provide value of project_id as an argument or Django setting."
            )

        _sitekey = use_setting("RECAPTCHA_ENTERPRISE_SITEKEY", sitekey)
        if _sitekey is None:
            raise ImproperlyConfigured(
                "Must provide value of sitekey as an argument or Django setting."
            )

        _access_token = use_setting("RECAPTCHA_ENTERPRISE_ACCESS_TOKEN", access_token)
        if _access_token is None:
            raise ImproperlyConfigured(
                "Must provide value of access_token as an argument or Django setting."
            )

        _required_score = use_setting(
            "RECAPTCHA_ENTERPRISE_REQUIRED_SCORE", required_score
        )
        if _required_score is None:
            raise ImproperlyConfigured(
                "Must provide value of required_score as an argument or Django setting."
            )
        if not 0.0 <= _required_score <= 1.0:
            raise ImproperlyConfigured(
                "The required score must be a value between 0.0 and 1.0."
            )

        if action and not _action_name_is_valid(action):
            raise ImproperlyConfigured(
                f"Action '{action}' contains disallowed character(s)."
            )

        super().__init__(**kwargs)
        self._project_id = _project_id
        self._sitekey = _sitekey
        self._access_token = _access_token
        self._action = action
        self._required_score = _required_score

        # set by calling add_additional_info()
        self._requested_uri: Optional[str] = None

        # set after successful verification
        self._score: Optional[float] = None

        self.widget.attrs["data-sitekey"] = sitekey
        if action:
            self.widget.attrs["data-action"] = action

    def validate(self, value: Optional[Any]) -> None:
        # fails if field is required and token is missing
        super().validate(value)

        # no validation is need if field is not required and token is missing
        if value is None:
            return

        try:
            verification_result = verify_enterprise_v1_token(
                self._project_id,
                self._sitekey,
                self._access_token,
                value,
                self._action,
                self._requested_uri,
            )
        except:
            raise ValidationError(
                "something went wrong while trying to validate token",
                code="captcha_error",
            )

        self._score = verification_result.score

        if not verification_result.is_okay(self._required_score):
            raise ValidationError("token failed verification", code="captcha_invalid")

    @property
    def score(self) -> Optional[float]:
        """Score of token after a successful verificaton attempt."""
        return self._score

    def add_additional_info(self, request: HttpRequest) -> None:
        """Adds additional information that is submitted with token verification attempt.

        :param request: HTTP request sent by user
        """
        self._requested_uri = request.build_absolute_uri()
