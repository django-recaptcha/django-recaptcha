import json

from django.conf import settings

from captcha._compat import (
    build_opener, ProxyHandler, PY2, Request, urlencode, urlopen, want_bytes
)
from captcha.decorators import generic_deprecation

DEFAULT_API_SSL_SERVER = "//www.google.com/recaptcha/api"  # made ssl agnostic
DEFAULT_API_SERVER = "//www.google.com/recaptcha/api"  # made ssl agnostic
DEFAULT_VERIFY_SERVER = "www.google.com"
DEFAULT_WIDGET_TEMPLATE = 'captcha/widget_nocaptcha.html'

API_SSL_SERVER = getattr(settings, "CAPTCHA_API_SSL_SERVER",
                         DEFAULT_API_SSL_SERVER)
API_SERVER = getattr(settings, "CAPTCHA_API_SERVER", DEFAULT_API_SERVER)
VERIFY_SERVER = getattr(
    settings, "CAPTCHA_VERIFY_SERVER", DEFAULT_VERIFY_SERVER
)
WIDGET_TEMPLATE = getattr(
    settings, "CAPTCHA_WIDGET_TEMPLATE", DEFAULT_WIDGET_TEMPLATE
)


RECAPTCHA_SUPPORTED_LANUAGES = ('en', 'nl', 'fr', 'de', 'pt', 'ru', 'es', 'tr')


class RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code


def request(*args, **kwargs):
    """
    Make a HTTP request with a proxy if configured.
    """
    if getattr(settings, 'RECAPTCHA_PROXY', False):
        proxy = ProxyHandler({
            'http': settings.RECAPTCHA_PROXY,
            'https': settings.RECAPTCHA_PROXY,
        })
        opener = build_opener(proxy)

        return opener.open(*args, **kwargs)
    else:
        return urlopen(*args, **kwargs)


def submit(recaptcha_challenge_field,
           recaptcha_response_field,
           private_key,
           remoteip,
           use_ssl=False):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    recaptcha_challenge_field -- The value of recaptcha_challenge_field
    from the form
    recaptcha_response_field -- The value of recaptcha_response_field
    from the form
    private_key -- your reCAPTCHA private key
    remoteip -- the user's ip address
    """

    if not (recaptcha_response_field and recaptcha_challenge_field and
            len(recaptcha_response_field) and len(recaptcha_challenge_field)):
        return RecaptchaResponse(
            is_valid=False,
            error_code='incorrect-captcha-sol'
        )

    params = urlencode({
        'secret': want_bytes(private_key),
        'response': want_bytes(recaptcha_response_field),
        'remoteip': want_bytes(remoteip),
    })
    if not PY2:
        params = params.encode('utf-8')

    verify_url = 'https://%s/recaptcha/api/siteverify' % VERIFY_SERVER
    req = Request(
        url=verify_url,
        data=params,
        headers={
            'Content-type': 'application/x-www-form-urlencoded',
            'User-agent': 'reCAPTCHA Python'
        }
    )

    httpresp = request(req)
    data = json.loads(httpresp.read().decode('utf-8'))
    return_code = data['success']
    return_values = [return_code, None]
    if return_code:
        return_code = 'true'
    else:
        return_code = 'false'
    httpresp.close()

    if (return_code == "true"):
        return RecaptchaResponse(is_valid=True)
    else:
        return RecaptchaResponse(is_valid=False, error_code=return_values[1])
