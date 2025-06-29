from string import ascii_letters, digits
from typing import Any, Optional

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.forms.fields import Field

from .client import verify_enterprise_v1_token
from .widgets import ReCAPTCHAEnterpriseNoWidget


# can only contain alphanumeric characters, slashes, and underscores
ACTION_ALLOWED_CHARS = set(ascii_letters + digits + "/" + "_")


def _action_name_is_valid(action) -> bool:
    """Checks whether name of a given action is valid.

    More information: https://cloud.google.com/recaptcha/docs/actions-website

    :param action: name of action
    """
    return all((ch in ACTION_ALLOWED_CHARS) for ch in action)


class ReCAPTCHAEnterpriseV1CheckboxField(Field):
    """Field that handles reCAPTCHA Enterprise V1 Checkbox tokens."""
    widget = ReCAPTCHAEnterpriseNoWidget  # TODO: change?

    def __init__(
        self,
        *,
        project_id: str,
        sitekey: str,
        access_token: str,
        action: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        :param project_id: identifier of GCP project
        :param sitekey: public key used to integrate reCAPTCHA
        :param access_token: private API key
        :param action: action associated with this reCAPTCHA field
        """
        if action and not _action_name_is_valid(action):
            raise ImproperlyConfigured(f"Action '{action}' contains disallowed character(s).")

        super().__init__(**kwargs)
        self._project_id = project_id
        self._sitekey = sitekey
        self._access_token = access_token
        self._action = action

        self.widget.attrs["data-sitekey"] = sitekey
        if action:
            self.widget.attrs["data-action"] = action


    def validate(self, value: Optional[Any]) -> None:
        super().validate(value)  # fails if token was missing from form data

        try:
            verification_result = verify_enterprise_v1_token(
                self._project_id,
                self._sitekey,
                self._access_token,
                value,
                self._action)
        except:
            raise ValidationError("sth went wrong", code="captcha_error")

        if not verification_result.is_okay():
            raise ValidationError("token was invalid", code="captcha_invalid")
