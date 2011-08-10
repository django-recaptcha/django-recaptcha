import sys

from django import forms
from django.conf import settings
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

from captcha import client
from captcha import utils
from captcha.widgets import ReCaptcha

class ReCaptchaField(forms.CharField):
    default_error_messages = {
        'captcha_invalid': _(u'Incorrect, please try again.')
    }

    def __init__(self, attrs={}, *args, **kwargs):
        """
        ReCaptchaField can accepts attributes which is a dictionary of attributes to be passed ot the ReCaptcha widget class.
        The widget will loop over any options added and create the RecaptchaOptions JavaScript variables as specified in 
        https://code.google.com/apis/recaptcha/docs/customization.html
        """
        self.widget = ReCaptcha(attrs=attrs)
        self.required = True
        super(ReCaptchaField, self).__init__(*args, **kwargs)

    def get_remote_ip(self):
        f = sys._getframe()
        while f:
            if f.f_locals.has_key('request'):
                request = f.f_locals['request']
                if request:
                    return request.META['REMOTE_ADDR']
            f = f.f_back

    def clean(self, values):
        super(ReCaptchaField, self).clean(values[1])
        recaptcha_challenge_value = smart_unicode(values[0])
        recaptcha_response_value = smart_unicode(values[1])
        check_captcha = client.submit(recaptcha_challenge_value, recaptcha_response_value, private_key=settings.RECAPTCHA_PRIVATE_KEY, remoteip=self.get_remote_ip(), use_ssl=utils.use_ssl())
        if not check_captcha.is_valid:
            raise forms.util.ValidationError(self.error_messages['captcha_invalid'])
        return values[0]
