import json
import uuid

from django.conf import settings
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from captcha._compat import urlencode
from captcha.constants import DEFAULT_RECAPTCHA_DOMAIN


class ReCaptchaBase(widgets.Widget):
    """
    Base widget to be used for Google ReCAPTCHA.

    public_key -- String value: can optionally be passed to not make use of the
        project wide Google Site Key.
    """
    recaptcha_response_name = "g-recaptcha-response"

    def __init__(self, api_params=None, *args, **kwargs):
        super(ReCaptchaBase, self).__init__(*args, **kwargs)
        self.uuid = uuid.uuid4().hex
        self.api_params = api_params or {}

    def value_from_datadict(self, data, files, name):
        return data.get(self.recaptcha_response_name, None)

    def get_context(self, name, value, attrs):
        context = super(ReCaptchaBase, self).get_context(name, value, attrs)
        params = urlencode(self.api_params)
        context.update({
            "public_key": self.attrs["data-sitekey"],
            "widget_uuid": self.uuid,
            "api_params": params,
            "recaptcha_domain": getattr(
                settings, "RECAPTCHA_DOMAIN", DEFAULT_RECAPTCHA_DOMAIN
            ),
        })
        return context

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super(ReCaptchaBase, self).build_attrs(base_attrs, extra_attrs)
        attrs["data-widget-uuid"] = self.uuid

        # Support the ability to override some of the Google data attrs.
        attrs["data-callback"] = base_attrs.get(
            "data-callback", "onSubmit_%s" % self.uuid
        )
        attrs["data-size"] = base_attrs.get("data-size", "normal")
        return attrs


class ReCaptchaV2Checkbox(ReCaptchaBase):
    template_name = "captcha/widget_v2_checkbox.html"


class ReCaptchaV2Invisible(ReCaptchaBase):
    template_name = "captcha/widget_v2_invisible.html"

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super(ReCaptchaV2Invisible, self).build_attrs(
            base_attrs, extra_attrs
        )

        # Invisible reCAPTCHA should not have another size
        attrs["data-size"] = "invisible"
        return attrs


class ReCaptchaV3(ReCaptchaBase):
    template_name = "captcha/widget_v3.html"

    def __init__(self, api_params=None, *args, **kwargs):
        super(ReCaptchaV3, self).__init__(
            api_params=api_params, *args, **kwargs
        )
        if not self.attrs.get("required_score", None):
            self.attrs["required_score"] = getattr(
                settings, "RECAPTCHA_REQUIRED_SCORE", None
            )

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super(ReCaptchaV3, self).build_attrs(
            base_attrs, extra_attrs
        )
        return attrs

    def value_from_datadict(self, data, files, name):
        return data.get(name)
