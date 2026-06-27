# Sandbox for django-recaptcha testing

This Django project exercises the various affordances offered by django-recaptcha.

- For each widget type there are several test pages to exercise them with different options
- Each page allows sending a bogus value in place of the captcha response, to check the failure mode
- Best used with own Google reCAPTCHA keys; falls back to the V2 testing keys that never fail (even when checking bogus captcha values).
