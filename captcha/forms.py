from registration.forms import RegistrationForm
from captcha.fields import ReCaptchaField

class RegistrationFormCaptcha(RegistrationForm):
    """
    My modification of the ReCaptchaField adds the ability to pass
    a dictionary of attributes to the ReCaptcha widget class.
    The widget will then loop over any options added, and create the
    RecaptchaOptions JavaScript variable.
    
    This depends on my patch of the recaptcha Python client, which I have included
    in the repo (captcha.py). I've also included a patch file (enable_recaptcha_options_patch.txt)
    """
    captcha = ReCaptchaField(attrs={'options' : {'theme' : 'clean'}})
