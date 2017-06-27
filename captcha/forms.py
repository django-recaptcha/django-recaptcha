from django.contrib.admin.forms import AdminAuthenticationForm

from .fields import ReCaptchaField


class ReCAPTCHAAdminAuthenticationForm(AdminAuthenticationForm):
    captcha = ReCaptchaField()
