import os
import socket
import sys
import warnings

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from captcha import client
from captcha.constants import TEST_PRIVATE_KEY, TEST_PUBLIC_KEY
from captcha.widgets import ReCaptchaV2Checkbox, ReCaptchaBase


class ReCaptchaField(forms.CharField):
    widget = ReCaptchaV2Checkbox
    default_error_messages = {
        "captcha_invalid": _("Incorrect, please try again."),
        "captcha_error": _("Error verifying input, please try again."),
    }

    def __init__(self, public_key=None, private_key=None, use_ssl=None,
                 *args, **kwargs):
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

        # Setup instance variables.
        self.private_key = private_key or getattr(
            settings, "RECAPTCHA_PRIVATE_KEY", TEST_PRIVATE_KEY)
        self.public_key = public_key or getattr(
            settings, "RECAPTCHA_PUBLIC_KEY", TEST_PUBLIC_KEY)

        if self.private_key == TEST_PRIVATE_KEY or \
                self.public_key == TEST_PUBLIC_KEY:
            warnings.warn(
                "RECAPTCHA_PRIVATE_KEY or RECAPTCHA_PUBLIC_KEY is making use"
                " of the Google test keys and will not behave as expected in a"
                " production environment",
                RuntimeWarning,
                2
            )
        self.use_ssl = use_ssl if use_ssl is not None else getattr(
            settings, "RECAPTCHA_USE_SSL", True)

        # Update widget attrs with data-sitekey.
        self.widget.attrs["data-sitekey"] = self.public_key

    def get_remote_ip(self):
        f = sys._getframe()
        while f:
            request = f.f_locals.get("request")
            if request:
                remote_ip = request.META.get("REMOTE_ADDR", "")
                forwarded_ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
                ip = remote_ip if not forwarded_ip else forwarded_ip
                return ip
            f = f.f_back

    def validate(self, value):
        super(ReCaptchaField, self).validate(value)

        try:
            check_captcha = client.submit(
                "g-recaptcha-response",
                value,
                private_key=self.private_key,
                remoteip=self.get_remote_ip(),
                use_ssl=self.use_ssl
            )

        # TODO: Does not catch urllib2.HTTPError correctly
        except socket.error:  # Catch timeouts, etc
            raise ValidationError(
                self.error_messages["captcha_error"],
                code="captcha_error"
            )

        if not check_captcha.is_valid:
            raise ValidationError(
                self.error_messages["captcha_invalid"],
                code="captcha_invalid"
            )
