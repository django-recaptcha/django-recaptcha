import json
import uuid

from django.conf import settings
from django.forms import widgets
from django.utils.safestring import mark_safe

from captcha.client import API_SERVER, WIDGET_TEMPLATE

class ReCaptchaBase(widgets.Widget):
    """
    Base widget to be used for Google ReCAPTCHA.

    public_key -- String value: can optionally be passed to not make use of the
        project wide Google Site Key.
    """
    recaptcha_response_name = "g-recaptcha-response"

    def __init__(self, *args, **kwargs):
        super(ReCaptchaBase, self).__init__(*args, **kwargs)
        self.uuid = uuid.uuid4().hex

    def value_from_datadict(self, data, files, name):
        return data.get(self.recaptcha_response_name, None)

    def get_context(self, name, value, attrs):
        context = super(ReCaptchaBase, self).get_context(name, value, attrs)

        # TODO make use of django.utils.translation import get_language
        language = self.attrs.get("language", "en")
        context.update({
            "api_server": API_SERVER,
            "public_key": self.attrs["data-sitekey"],
            "language": language,
            "widget_uuid": self.uuid,
        })
        return context

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super(ReCaptchaBase, self).build_attrs(base_attrs, extra_attrs)
        attrs["data-widget-uuid"] = self.uuid

        # Support the ability to override some of the Google data attrs.
        attrs["data-callback"] = base_attrs.get("data-callback", "onSubmit_%s" % self.uuid)
        attrs["data-size"] = base_attrs.get("data-size", "normal")
        return attrs


class ReCaptchaV2Checkbox(ReCaptchaBase):
    template_name = "captcha/widget_v2_checkbox.html"


class ReCaptchaV2Invisible(ReCaptchaBase):
    template_name = "captcha/widget_v2_invisible.html"

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super(ReCaptchaV2Invisible, self).build_attrs(base_attrs, extra_attrs)

        # Invisible reCAPTCHA should not have another size
        attrs["data-size"] = "invisible"
        return attrs
