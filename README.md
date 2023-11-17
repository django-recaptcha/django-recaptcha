# Django reCAPTCHA <!-- omit from toc -->

**Django reCAPTCHA form field/widget integration app.**

[![PyPI latest version](https://img.shields.io/pypi/v/django-recaptcha.svg)](https://pypi.org/project/django-recaptcha/)
[![PyPI monthly downloads](https://img.shields.io/pypi/dm/django-recaptcha.svg)](https://pypi.org/project/django-recaptcha/)
[![CI status](https://github.com/torchbox/django-recaptcha/workflows/CI/badge.svg)](https://github.com/torchbox/django-recaptcha/actions)
[![Coverage](https://coveralls.io/repos/github/torchbox/django-recaptcha/badge.svg?branch=main)](https://coveralls.io/github/torchbox/django-recaptcha?branch=main)

> [!NOTE]
> django-recaptcha supports Google reCAPTCHA V2 - Checkbox (Default), Google reCAPTCHA V2 - Invisible and Google reCAPTCHA V3. Please look at the widgets section for more information.
>
> Django reCAPTCHA uses a modified version of the [Python reCAPTCHA client](http://pypi.python.org/pypi/recaptcha-client) which is included in the package as `client.py`.

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Fields](#fields)
  - [Widgets](#widgets)
  - [reCAPTCHA V3 Score](#recaptcha-v3-score)
  - [reCAPTCHA V3 Action](#recaptcha-v3-action)
  - [Local Development and Functional Testing](#local-development-and-functional-testing)
- [Credits](#credits)

## Requirements

Tested with:

- Python: 3.8, 3.9, 3.10, 3.11
- Django: 3.2, 4.1, 4.2
- You can view the [Python-Django support matrix
  here](https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django)

This package only supports modern, “evergreen” desktop and mobile
browsers. For IE11 support, make sure to add a [polyfill for
Element.closest](https://developer.mozilla.org/en-US/docs/Web/API/Element/closest#Polyfill).

## Installation

1.  [Sign up for reCAPTCHA](https://www.google.com/recaptcha/intro/index.html).

2.  Install with `pip install django-recaptcha`.

3.  Add `'django_recaptcha'` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = [
    ...,
    'django_recaptcha',
    ...
]
```

4.  Add the Google reCAPTCHA keys generated in step 1 to your Django
    production settings with `RECAPTCHA_PUBLIC_KEY` and
    `RECAPTCHA_PRIVATE_KEY`. Note that omitting these settings will
    default to a set of test keys refer to [Local Development and
    Functional Testing](#local-development-and-functional-testing) for
    more information.

For example:

```python
RECAPTCHA_PUBLIC_KEY = 'MyRecaptchaKey123'
RECAPTCHA_PRIVATE_KEY = 'MyRecaptchaPrivateKey456'
```

These can also be specified per field by passing the `public_key`
or `private_key` parameters to `ReCaptchaField` - see field usage
below.

5.  (OPTIONAL) If you require a proxy, add a `RECAPTCHA_PROXY` setting
    (dictionary of proxies), for example:

```python
RECAPTCHA_PROXY = {'http': 'http://127.0.0.1:8000', 'https': 'https://127.0.0.1:8000'}
```

6.  (OPTIONAL) In the event `www.google.com` is not accessible the
    `RECAPTCHA_DOMAIN` setting can be changed to `www.recaptcha.net` as
    per the [reCAPTCHA
    FAQ](https://developers.google.com/recaptcha/docs/faq#can-i-use-recaptcha-globally):

```python
RECAPTCHA_DOMAIN = 'www.recaptcha.net'
```

This will change the Google JavaScript api domain as well as the client
side field verification domain.

## Usage

### Fields

The quickest way to add reCAPTCHA to a form is to use the included
`ReCaptchaField` field class. A `ReCaptchaV2Checkbox` will be rendered
by default. For example:

```python
from django import forms
from django_recaptcha.fields import ReCaptchaField

class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField()
```

Be sure to include the captcha field in your forms. There are many ways
to add fields to forms in Django. We recommend you refer to the [form
rendering
options](https://docs.djangoproject.com/en/dev/topics/forms/#form-rendering-options)
and [rendering fields
manually](https://docs.djangoproject.com/en/dev/topics/forms/#rendering-fields-manually)
sections of the [official Django documentation for
forms](https://docs.djangoproject.com/en/dev/topics/forms).

To allow for runtime specification of keys you can optionally pass the
`private_key` or `public_key` parameters to the constructor. For
example:

```python
captcha = ReCaptchaField(
    public_key='76wtgdfsjhsydt7r5FFGFhgsdfytd656sad75fgh',
    private_key='98dfg6df7g56df6gdfgdfg65JHJH656565GFGFGs',
)
```

If specified, these parameters will be used instead of your reCAPTCHA
project settings.

### Widgets

There are three widgets that can be used with the `ReCaptchaField`
class:

- `ReCaptchaV2Checkbox` for [Google reCAPTCHA V2 - Checkbox](https://developers.google.com/recaptcha/docs/display)
- `ReCaptchaV2Invisible` for [Google reCAPTCHA V2 - Invisible](https://developers.google.com/recaptcha/docs/invisible)
- `ReCaptchaV3` for [Google reCAPTCHA V3](https://developers.google.com/recaptcha/docs/v3)

To make use of widgets other than the default Google reCAPTCHA V2 -
Checkbox widget, simply replace the `ReCaptchaField` widget. For
example:

```python
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible

class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
```

The reCAPTCHA widget supports several [data
attributes](https://developers.google.com/recaptcha/docs/display#render_param)
that customize the behaviour of the widget, such as `data-theme`,
`data-size`, etc. You can forward these options to the widget by passing
an `attrs` parameter to the widget, containing a dictionary of options.
For example:

```python
captcha = fields.ReCaptchaField(
    widget=widgets.ReCaptchaV2Checkbox(
        attrs={
            'data-theme': 'dark',
            'data-size': 'compact',
        }
    )
)
# The ReCaptchaV2Invisible widget
# ignores the "data-size" attribute in favor of 'data-size="invisible"'
```

The reCAPTCHA api supports several
[parameters](https://developers.google.com/recaptcha/docs/display#js_param).
To customise the parameters that get sent along pass an `api_params`
parameter to the widget, containing a dictionary of options. For
example:

```python
captcha = fields.ReCaptchaField(
    widget=widgets.ReCaptchaV2Checkbox(
        api_params={'hl': 'cl', 'onload': 'onLoadFunc'}
    )
)
# The dictionary is urlencoded and appended to the reCAPTCHA api url.
```

By default, the widgets provided only supports a single form with a
single widget on each page.

The language can be set with the 'h1' parameter, look at [language
codes](https://developers.google.com/recaptcha/docs/language) for the
language code options. Note that translations need to be added to this
package for the errors to be shown correctly. Currently the package has
error translations for the following language codes: es, fr, nl, pl,
pt_BR, ru, zh_CN, zh_TW

However, the JavaScript used by the widgets can easily be overridden in
the templates.

The templates are located in:

- `django_recaptcha/includes/js_v2_checkbox.html` for overriding the reCAPTCHA V2 - Checkbox template
- `django_recaptcha/includes/js_v2_invisible.html` for overriding the reCAPTCHA V2 - Invisible template
- `django_recaptcha/includes/js_v3.html` for overriding the reCAPTCHA V3 template

For more information about overriding templates look at [Django's template override](https://docs.djangoproject.com/en/4.2/howto/overriding-templates/)

### reCAPTCHA V3 Score

As of version 3, reCAPTCHA also returns a score value. This can be used
to determine the likelihood of the page interaction being a bot. See the Google [documentation](https://developers.google.com/recaptcha/docs/v3#score)
for more details.

To set a project wide score limit use the `RECAPTCHA_REQUIRED_SCORE` setting.

For example:

```python
RECAPTCHA_REQUIRED_SCORE = 0.85
```

For per field, runtime, specification the attribute can also be passed to the widget:

```python
captcha = fields.ReCaptchaField(
    widget=ReCaptchaV3(
        attrs={
            'required_score':0.85,
            ...
        }
    )
)
```

In the event the score does not meet the requirements, the field
validation will fail as expected and an error message will be logged.

### reCAPTCHA V3 Action

[Google's reCAPTCHA V3 API supports passing an action value](https://developers.google.com/recaptcha/docs/v3#actions).
Actions allow you to tie reCAPTCHA validations to a specific form on your site for analytical purposes, enabling you to perform risk analysis per form. This will allow you to make informed decisions about adjusting the score threshold for certain forms because abusive behavior can vary depending on the nature of the form.

To set the action value, pass an `action` argument when instantiating the ReCaptcha
widget. Be careful to only use alphanumeric characters, slashes and underscores as stated in the reCAPTCHA documentation.

```python
captcha = fields.ReCaptchaField(
    widget=widgets.ReCaptchaV3(
        action='signup'
    )
)
```

Setting an action is entirely optional. If you don't specify an action, no action will be passed to the reCAPTCHA V3 API.

### Local Development and Functional Testing

If `RECAPTCHA_PUBLIC_KEY` and `RECAPTCHA_PRIVATE_KEY` are not set,
django-recaptcha will use [Google's test
keys](https://developers.google.com/recaptcha/docs/faq) instead. These
cannot be used in production since they always validate to true and a
warning will be shown on the reCAPTCHA. Google's test keys only work for
reCAPTCHA version 2.

To bypass the security check that prevents the test keys from being used
unknowingly add
`SILENCED_SYSTEM_CHECKS = [..., 'django_recaptcha.recaptcha_test_key_error', ...]`
to your settings, here is an example:

```python
SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']
```

If you want to mock the call to Google's servers altogether, have a look
at
[test_fields.py](https://github.com/torchbox/django-recaptcha/blob/main/captcha/tests/test_fields.py):

```python
from unittest.mock import patch
from django.test import TestCase
from django_recaptcha.client import RecaptchaResponse

class TestFields(TestCase):
    @patch("django_recaptcha.fields.client.submit")
    def test_client_success_response(self, mocked_submit):
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        ...
```

## Credits

Originally developed by [Praekelt Consulting](https://github.com/praekelt/django-recaptcha)

Inspired Marco Fucci's blogpost titled [Integrating reCAPTCHA with Django](http://www.marcofucci.com/tumblelog/26/jul/2009/integrating-recaptcha-with-django)

`client.py` taken from [recaptcha-client](http://pypi.python.org/pypi/recaptcha-client) licensed MIT/X11 by Mike Crawford.

reCAPTCHA copyright 2012 Google.
