import os

from django import forms
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha import constants
from django_recaptcha import widgets


VARIANTS = {}


class Variant(View):
    Form: type

    def __init_subclass__(cls):
        if not cls.__name__.startswith("_"):
            VARIANTS[cls.__name__] = cls

    @classmethod
    def url(cls):
        return reverse("variant", kwargs={"slug": cls.__name__})

    # TODO this should come from the widget's `recaptcha_response_name` field,
    # but it's only accurate for V2 captchas.
    data_field_name = "g-recaptcha-response"

    def get(self, request):
        return self.render(request, self.Form())

    def post(self, request):
        form = self.Form(request.POST)
        if form.is_valid():
            messages.success(request, "👍")
            return redirect(self.url())

        messages.error(request, "👎")
        return self.render(request, form)

    def render(self, request, form):
        context = {
            "form": form,
            "variant_name": type(self).__name__,
            "doc": self.__doc__,
            "VARIANTS": VARIANTS,
            "fake": "fake" in request.GET,
            "data_field_name": self.data_field_name,
        }
        return render(request, "home.html", context)


def get_keys(name):
    return {
        "public_key": os.environ.get(f"RECAPTCHA_{name}_PUBLIC_KEY", constants.TEST_PUBLIC_KEY),
        "private_key": os.environ.get(f"RECAPTCHA_{name}_PRIVATE_KEY", constants.TEST_PRIVATE_KEY),
    }


class V2Checkbox(Variant):
    """The standard "I'm not a robot" checkbox."""

    class Form(forms.Form):
        captcha = ReCaptchaField(
            widget=widgets.ReCaptchaV2Checkbox,
            **get_keys("V2_CHECKBOX"),
        )


class V2CheckboxApiParams(Variant):
    """Checkbox with custom api_params: Latin locale and an onload callback."""

    class Form(forms.Form):
        captcha = ReCaptchaField(
            widget=widgets.ReCaptchaV2Checkbox(api_params={"hl": "la", "onload": "example_onload"}),
            **get_keys("V2_CHECKBOX"),
        )


class V2Invisible(Variant):
    """Invisible badge; validation triggers on submit."""

    class Form(forms.Form):
        captcha = ReCaptchaField(
            widget=widgets.ReCaptchaV2Invisible,
            **get_keys("V2_INVISIBLE"),
        )


class _BaseV3Variant(Variant):
    data_field_name = "captcha"


class V3(_BaseV3Variant):
    """Score-based, with no user interaction."""

    class Form(forms.Form):
        captcha = ReCaptchaField(
            widget=widgets.ReCaptchaV3,
            **get_keys("V3"),
        )


class V3CustomRequiredScore(_BaseV3Variant):
    """V3 with a near-zero required_score, so almost anything passes."""

    class Form(forms.Form):
        captcha = ReCaptchaField(
            widget=widgets.ReCaptchaV3(required_score=0.0001),
            **get_keys("V3"),
        )


class V3CustomAction(_BaseV3Variant):
    """V3 tagging submissions with a custom action name."""

    class Form(forms.Form):
        captcha = ReCaptchaField(
            widget=widgets.ReCaptchaV3(action="sandbox"),
            **get_keys("V3"),
        )


def home(request):
    return redirect("variant", slug=next(iter(VARIANTS)))


def variant(request, slug):
    if slug not in VARIANTS:
        raise Http404
    return VARIANTS[slug].as_view()(request)
