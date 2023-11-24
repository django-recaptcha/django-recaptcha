import uuid
from urllib.parse import urlencode

from django.conf import settings
from django.forms import widgets
from django.templatetags.static import static

from django_recaptcha.constants import DEFAULT_RECAPTCHA_DOMAIN


class ReCaptchaBase(widgets.Widget):
    """
    Base widget to be used for Google ReCAPTCHA.

    public_key -- String value: can optionally be passed to not make use of the
        project wide Google Site Key.
    """

    recaptcha_response_name = "g-recaptcha-response"

    def __init__(self, api_params=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = uuid.uuid4().hex
        self.api_params = api_params or {}

        if not self.attrs.get("class", None):
            self.attrs["class"] = "g-recaptcha"

    def value_from_datadict(self, data, files, name):
        return data.get(self.recaptcha_response_name, None)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        params = urlencode(self.api_params)
        context.update(
            {
                "public_key": self.attrs["data-sitekey"],
                "widget_uuid": self.uuid,
                "api_params": params,
                "recaptcha_domain": getattr(
                    settings, "RECAPTCHA_DOMAIN", DEFAULT_RECAPTCHA_DOMAIN
                ),
                "script_url": self.script_name,
            }
        )
        return context

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["data-widget-uuid"] = self.uuid

        # Support the ability to override some of the Google data attrs.
        attrs["data-callback"] = base_attrs.get(
            "data-callback", "onSubmit_%s" % self.uuid
        )
        attrs["data-size"] = base_attrs.get("data-size", "normal")
        return attrs


class ReCaptchaV2Checkbox(ReCaptchaBase):
    template_name = "django_recaptcha/widget_v2_checkbox.html"
    script_name = static("django_recaptcha/js/widget_v2_checkbox.js")


class ReCaptchaV2Invisible(ReCaptchaBase):
    template_name = "django_recaptcha/widget_v2_invisible.html"
    script_name = static("django_recaptcha/js/widget_v2_invisible.js")

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)

        # Invisible reCAPTCHA should not have another size
        attrs["data-size"] = "invisible"
        return attrs


class ReCaptchaV3(ReCaptchaBase):
    input_type = "hidden"
    template_name = "django_recaptcha/widget_v3.html"
    script_name = static("django_recaptcha/js/widget_v3.js")

    def __init__(self, api_params=None, action=None, *args, **kwargs):
        super().__init__(api_params=api_params, *args, **kwargs)
        if not self.attrs.get("required_score", None):
            self.attrs["required_score"] = getattr(
                settings, "RECAPTCHA_REQUIRED_SCORE", None
            )
        self.action = action

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        if self.action:
            attrs["data-action"] = self.action
        return attrs

    def value_from_datadict(self, data, files, name):
        return data.get(name)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context.update({"action": self.action})
        return context
