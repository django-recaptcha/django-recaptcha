from django.conf import settings

def use_ssl():
    return getattr(settings, 'RECAPTCHA_USE_SSL', False)
