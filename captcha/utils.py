from django.conf import settings

def use_ssl():
    if 'RECAPTCHA_USE_SSL' in settings.__members__:
        return settings.RECAPTCHA_USE_SSL
    else:
        return False
