from typing import Any, Optional

from django.core.exceptions import ValidationError
from django.forms.fields import Field

from .client import verify_enterprise_v1_token
from .widgets import ReCAPTCHAEnterpriseNoWidget


class ReCAPTCHAEnterpriseV1CheckboxField(Field):
    """Field that handles reCAPTCHA Enterprise V1 Checkbox tokens."""
    widget = ReCAPTCHAEnterpriseNoWidget  # TODO: change?

    def __init__(
        self,
        *,
        project_id: str,
        sitekey: str,
        access_token: str,
        **kwargs: Any,
    ) -> None:
        """
        :param project_id: identifier of GCP project
        :param sitekey: public key used to integrate reCAPTCHA
        :param access_token: private API key
        """
        super().__init__(**kwargs)
        self._project_id = project_id
        self._sitekey = sitekey
        self._access_token = access_token
        self.widget.attrs["data-sitekey"] = sitekey

    def validate(self, value: Optional[Any]) -> None:
        super().validate(value)  # fails if token was missing from form data

        try:
            verification_result = verify_enterprise_v1_token(
                self._project_id,
                self._sitekey,
                self._access_token,
                value)
        except:
            raise ValidationError("sth went wrong", code="captcha_error")

        if not verification_result.is_okay():
            raise ValidationError("token was invalid", code="captcha_invalid")
