Django reCAPTCHA
================
**Django reCAPTCHA form field/widget integration app.**

.. image:: https://travis-ci.org/praekelt/django-recaptcha.svg?branch=develop
    :target: https://travis-ci.org/praekelt/django-recaptcha
.. image:: https://coveralls.io/repos/github/praekelt/django-recaptcha/badge.svg?branch=develop
    :target: https://coveralls.io/github/praekelt/django-recaptcha?branch=develop
.. image:: https://badge.fury.io/py/django-recaptcha.svg
    :target: https://badge.fury.io/py/django-recaptcha

.. contents:: Contents
    :depth: 5

Django reCAPTCHA uses a modified version of the `Python reCAPTCHA client
<http://pypi.python.org/pypi/recaptcha-client>`_ which is included in the
package as ``client.py``.


Requirements
------------

Tested with:

* Python: 2.7, 3.5, 3.6, 3.7
* Django: 1.11, 2.0, 2.1

Installation
------------

#. `Sign up for reCAPTCHA <https://www.google.com/recaptcha/intro/index.html>`_.

#. Install with ``pip install django-recaptcha``.

#. Add ``'captcha'`` to your ``INSTALLED_APPS`` setting.

    .. code-block:: python

        INSTALLED_APPS = [
            ...,
            'captcha',
            ...
        ]

#. Add the keys reCAPTCHA have given you to your Django production settings (leave development settings blank to use the default test keys) as
    ``RECAPTCHA_PUBLIC_KEY`` and ``RECAPTCHA_PRIVATE_KEY``. For example:

    .. code-block:: python

        RECAPTCHA_PUBLIC_KEY = 'MyRecaptchaKey123'
        RECAPTCHA_PRIVATE_KEY = 'MyRecaptchaPrivateKey456'

    These can also be specificied per field by passing the ``public_key`` or
    ``private_key`` parameters to ``ReCaptchaField`` - see field usage below.

#. If you require a proxy, add a ``RECAPTCHA_PROXY`` setting, for example:

    .. code-block:: python

        RECAPTCHA_PROXY = 'http://127.0.0.1:8000'

Usage
-----

Fields
~~~~~~

The quickest way to add reCAPTCHA to a form is to use the included
``ReCaptchaField`` field class. A ``ReCaptchaV2Checkbox`` widget will be rendered with
the field validating itself without any further action required. For example:

.. code-block:: python

    from django import forms
    from captcha.fields import ReCaptchaField

    class FormWithCaptcha(forms.Form):
        captcha = ReCaptchaField()


To allow for runtime specification of keys you can optionally pass the
``private_key`` or ``public_key`` parameters to the constructor. For example:

.. code-block:: python

    captcha = ReCaptchaField(
        public_key='76wtgdfsjhsydt7r5FFGFhgsdfytd656sad75fgh',
        private_key='98dfg6df7g56df6gdfgdfg65JHJH656565GFGFGs',
    )

If specified these parameters will be used instead of your reCAPTCHA project settings.

Widgets
~~~~~~~

There are two widgets that can be used with the ``ReCaptchaField``;

    ``ReCaptchaV2Checkbox`` for Google reCAPTCHA V2 - Checkbox

    ``ReCaptchaV2Invisible`` for Google reCAPTCHA V2 - Invisible

To make use of widgets other than the Google reCAPTCHA V2 - Checkbox, simply replace the ``ReCaptchaField`` widget. For example:

.. code-block:: python

    from django import forms
    from captcha.fields import ReCaptchaField
    from captcha.widgets import ReCaptchaV2Invisible

    class FormWithCaptcha(forms.Form):
        captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

The reCAPTCHA widget supports several `Javascript options variables
<https://developers.google.com/recaptcha/docs/display#js_param>`_ that
customize the behaviour of the widget, such as ``data-theme`` and ``language``. You can
forward these options to the widget by passing an ``attrs`` parameter to the
widget, containing a dictionary of options. For example:

.. code-block:: python

    captcha = fields.ReCaptchaField(
        widget=widgets.ReCaptchaV2Checkbox(
            attrs={
                'data-theme': 'dark',
                'data-size': 'compact',
                'language': 'cs'
            }
        )
    )
    # The ReCaptchaV2Invisible widget, 
    # ignores the "data-size" attribute in favor of 'data-size="invisible"'

By default the widgets provided only support a single form with a single widget per page.

However the JavaScript used by the widgets are in a separate template directory, that gets included at the top of the widget templates.

These can easily be overridden to suit your project needs, by making use of `Django's template override <https://docs.djangoproject.com/en/2.1/howto/overriding-templates/>`_:

    ``captcha/includes/js_v2_checkbox.html`` for the reCAPTCHA V2 - Checkbox

    ``captcha/includes/js_v2_invisible.html`` for the reCAPTCHA V2 - Invisible


Local Development and Functional Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Google provides test keys which are set as the default for ``RECAPTCHA_PUBLIC_KEY`` and ``RECAPTCHA_PRIVATE_KEY``. These cannot be used in production since they always validate to true and a warning will be shown on the reCAPTCHA.


Disabling SSL
~~~~~~~~~~~~~

This library used to not use SSL by default, but now it does. You can disable
this if required, but you should think long and hard about it before you do so!

You can disable it by setting ``RECAPTCHA_USE_SSL = False`` in your Django
settings, or by passing ``use_ssl=False`` to the constructor of
``ReCaptchaField``.


Credits
-------
Inspired Marco Fucci's blogpost titled `Integrating reCAPTCHA with Django
<http://www.marcofucci.com/tumblelog/26/jul/2009/integrating-recaptcha-with-django>`_


``client.py`` taken from `recaptcha-client
<http://pypi.python.org/pypi/recaptcha-client>`_ licenced MIT/X11 by Mike
Crawford.

reCAPTCHA copyright 2012 Google.
