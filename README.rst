Inspired by
===========
Marco Fucci @ http://www.marcofucci.com/tumblelog/26/jul/2009/integrating-recaptcha-with-django/

Modified by
===========
Brandon Taylor @ http://btaylordesign.com/ email: btaylordesign@gmail.com
This version of django-recaptcha uses a modified version of the Python ReCaptcha client: http://pypi.python.org/pypi/recaptcha-client
which is included in the repo as: captcha.py

The Python ReCaptcha client has several options that can be set via a JavaScript variable called "RecaptchaOptions", such as 'theme' and 'lang'.
I've modified the django-recaptcha ReCaptchaField to accept an "attr" parameter that can contain a dictionary of these options, e.g.:

recaptcha = ReCaptchaField(attrs={'options' : {'theme' : 'clean'}})

The attrs then get passed to a modified ReCaptcha widget class that hands off the attrs to the render method of the widget.
The captcha client takes the key/value pairs for the options key, iterates over them, and writes out the RecaptchaOptions value in JavaScript.

Now the options for the ReCaptcha client can be set programmatically, like any other Django widget.

I haven't enabled all possible combinations or nesting of properties, but these modifications will allow
you to use themes for ReCaptcha as defined at: http://code.google.com/apis/recaptcha/docs/customization.html

Happy Coding!