from registration.forms import RegistrationForm
from captcha.fields import ReCaptchaField

class RegistrationFormCaptcha(RegistrationForm):
    captcha = ReCaptchaField()
