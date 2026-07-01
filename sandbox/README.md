# Sandbox for django-recaptcha testing

This Django project exercises the functionality of django-recaptcha.

- For each widget type there are several test pages to exercise them with different options
- Each page allows sending a bogus value in place of the captcha response, to check the failure mode
- Best used with own Google reCAPTCHA keys; falls back to the V2 testing keys that never fail (even when checking bogus captcha values).

## Usage
After cloning `django-recaptcha`, run these commands at the repository root.

To supply your own reCAPTCHA keys, you can install [direnv](https://direnv.net/), and create an `.envrc` file:

```shell
export RECAPTCHA_V2_CHECKBOX_PUBLIC_KEY="..."
export RECAPTCHA_V2_CHECKBOX_PRIVATE_KEY="..."
export RECAPTCHA_V2_INVISIBLE_PUBLIC_KEY="..."
export RECAPTCHA_V2_INVISIBLE_PRIVATE_KEY="..."
export RECAPTCHA_V3_PUBLIC_KEY="..."
export RECAPTCHA_V3_PRIVATE_KEY="..."
```

Then create a virtualenv, install `django-recaptcha` in "editable" mode and run the development server. If you are using [uv](https://docs.astral.sh/uv/):

```shell
uv venv
uv pip install -e .
source .venv/bin/activate
./sandbox/manage.py runserver
```
