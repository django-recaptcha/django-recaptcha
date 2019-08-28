import hashlib
import logging
import os
import socket
import sys
import warnings

from django import forms
from django.conf import settings
from django.core import signing
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from captcha import client
from captcha._compat import HTTPError, urlencode
from captcha.constants import TEST_PRIVATE_KEY, TEST_PUBLIC_KEY
from captcha.widgets import ReCaptchaV2Checkbox, ReCaptchaBase, ReCaptchaV3


logger = logging.getLogger(__name__)


class ReCaptchaField(forms.CharField):
    widget = ReCaptchaV2Checkbox
    default_error_messages = {
        "captcha_invalid": _("Error verifying reCAPTCHA, please try again."),
        "captcha_error": _("Error verifying reCAPTCHA, please try again."),
    }
    cache_key_salt = "recaptcha_field_result_cache"
    cache_key_base = "%s-captcha-cached-result"

    def __init__(self, public_key=None, private_key=None,
                 wizard_persist_is_valid=None, *args, **kwargs):
        """
        ReCaptchaField can accepts attributes which is a dictionary of
        attributes to be passed to the ReCaptcha widget class. The widget will
        loop over any options added and create the RecaptchaOptions
        JavaScript variables as specified in
        https://developers.google.com/recaptcha/docs/display#render_param
        """
        super(ReCaptchaField, self).__init__(*args, **kwargs)

        if not isinstance(self.widget, ReCaptchaBase):
            raise ImproperlyConfigured(
                "captcha.fields.ReCaptchaField.widget"
                " must be a subclass of captcha.widgets.ReCaptchaBase"
            )

        # reCAPTCHA fields are always required.
        self.required = True
        self.wizard_persist_is_valid = wizard_persist_is_valid or False

        # Setup instance variables.
        self.private_key = private_key or getattr(
            settings, "RECAPTCHA_PRIVATE_KEY", TEST_PRIVATE_KEY)
        self.public_key = public_key or getattr(
            settings, "RECAPTCHA_PUBLIC_KEY", TEST_PUBLIC_KEY)

        # Update widget attrs with data-sitekey.
        self.widget.attrs["data-sitekey"] = self.public_key

    def request(self):
        f = sys._getframe()
        while f:
            request = f.f_locals.get("request")
            if request:
                return request
            f = f.f_back
        return None

    def get_remote_ip(self):
        request = self.request()
        if request:
            remote_ip = request.META.get("REMOTE_ADDR", "")
            forwarded_ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
            ip = remote_ip if not forwarded_ip else forwarded_ip
            return ip

    def _cache_key(self, path):
        return hashlib.sha256(
            (self.cache_key_base % path).encode("utf-8")
        ).hexdigest()

    def _get_result(self):
        is_valid = False
        request = self.request()
        token = request.session.get(
            self._cache_key(request.get_full_path()), None
        )
        if not token:
            return is_valid

        # Make use of the signing package to ensure the token has not expired.
        try:
            # TODO: max_age, global setting or field kwarg
            is_valid = signing.loads(
                token,
                salt=self.cache_key_salt,
                max_age=10
            )
        except signing.SignatureExpired:
            return is_valid

        return is_valid

    def _set_result(self):
        request = self.request()
        token = signing.dumps(
            True,
            salt=self.cache_key_salt
        )
        request.session[self._cache_key(request.get_full_path())] = token

    def validate(self, value):
        # Do not do any further validation. This field has already
        # been validated successfully.
        # NOTE: Needs to happen before super, not all the widget templates have
        # inputs that actually get updated, as such required and additional
        # checks will also fail.
        if self.wizard_persist_is_valid and self._get_result() is True:
            return None

        super(ReCaptchaField, self).validate(value)

        try:
            check_captcha = client.submit(
                recaptcha_response=value,
                private_key=self.private_key,
                remoteip=self.get_remote_ip(),
            )

        except HTTPError:  # Catch timeouts, etc
            raise ValidationError(
                self.error_messages["captcha_error"],
                code="captcha_error"
            )

        if not check_captcha.is_valid:
            logger.error(
                "ReCAPTCHA validation failed due to: %s" %
                check_captcha.error_codes
            )
            raise ValidationError(
                self.error_messages["captcha_invalid"],
                code="captcha_invalid"
            )

        required_score = self.widget.attrs.get("required_score")
        if required_score:
            # Our score values need to be floats, as that is the expected
            # response from the Google endpoint. Rather than ensure that on
            # the widget, we do it on the field to better support user
            # subclassing of the widgets.
            required_score = float(required_score)

            # If a score was expected but non was returned, default to a 0,
            # which is the lowest score that it can return. This is to do our
            # best to assure a failure here, we can not assume that a form
            # that needed the threshold should be valid if we didn't get a
            # value back.
            score = float(check_captcha.extra_data.get("score", 0))

            if required_score > score:
                logger.error(
                    "ReCAPTCHA validation failed due to its score of %s"
                    " being lower than the required amount." % score
                )
                raise ValidationError(
                    self.error_messages["captcha_invalid"],
                    code="captcha_invalid"
                )

        if self.wizard_persist_is_valid:
            self._set_result()
