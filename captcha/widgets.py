from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from captcha import client
from captcha import utils

class ReCaptcha(forms.widgets.Widget):
    recaptcha_challenge_name = 'recaptcha_challenge_field'
    recaptcha_response_name = 'recaptcha_response_field'

    def __init__(self, *args, **kwargs):
        self.attrs = kwargs.get('attrs', {})
        super(ReCaptcha, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        return mark_safe(u'%s' % client.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, self.attrs, use_ssl=utils.use_ssl()))

    def value_from_datadict(self, data, files, name):
        return [data.get(self.recaptcha_challenge_name, None),
            data.get(self.recaptcha_response_name, None)]
