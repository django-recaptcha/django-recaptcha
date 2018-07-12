import json

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from .client import API_SERVER, ASYNC, DEFER, WIDGET_TEMPLATE


class ReCaptcha(forms.widgets.Widget):
    if getattr(settings, 'NOCAPTCHA', False):
        recaptcha_response_name = 'g-recaptcha-response'
        recaptcha_challenge_name = 'g-recaptcha-response'
    else:
        recaptcha_challenge_name = 'recaptcha_challenge_field'
        recaptcha_response_name = 'recaptcha_response_field'

    template_name = WIDGET_TEMPLATE

    def __init__(self, public_key, *args, **kwargs):
        super(ReCaptcha, self).__init__(*args, **kwargs)
        self.public_key = public_key

    def value_from_datadict(self, data, files, name):
        return [
            data.get(self.recaptcha_challenge_name, None),
            data.get(self.recaptcha_response_name, None)
        ]

    def get_context(self, name, value, attrs):

        try:
            lang = attrs['lang']
        except KeyError:
            # Get the generic language code
            lang = get_language().split('-')[0]

        try:
            context = super(ReCaptcha, self).get_context(name, value, attrs)
        except AttributeError:
            context = {
                "widget": {
                    "attrs": self.build_attrs(attrs)
                }
            }
        context.update({
            'async': ASYNC,
            'defer': DEFER,
            'api_server': API_SERVER,
            'public_key': self.public_key,
            'lang': lang,
            'options': mark_safe(json.dumps(self.attrs, indent=2)),
        })
        return context
