Django reCAPTCHA
================
**Django reCAPTCHA form field/widget integration app.**

.. image:: https://travis-ci.org/praekelt/django-recaptcha.svg?branch=develop
    :target: https://travis-ci.org/praekelt/django-recaptcha
.. image:: https://coveralls.io/repos/github/praekelt/django-recaptcha/badge.svg?branch=develop
    :target: https://coveralls.io/github/praekelt/django-recaptcha?branch=develop
.. image:: https://badge.fury.io/py/django-recaptcha.svg
    :target: https://badge.fury.io/py/django-recaptcha
.. image:: https://img.shields.io/pypi/pyversions/django-recaptcha.svg
    :target: https://pypi.python.org/pypi/django-recaptcha
.. image:: https://img.shields.io/pypi/djversions/django-recaptcha.svg
    :target: https://pypi.python.org/pypi/django-recaptcha
   
.. contents:: Contents
    :depth: 5

.. note::
   django-recaptcha supports Google reCAPTCHA V2 - Checkbox (Default), Google reCAPTCHA V2 - Invisible and Google reCAPTCHA V3 please look at the widgets section for more information.

   Django reCAPTCHA uses a modified version of the `Python reCAPTCHA client <http://pypi.python.org/pypi/recaptcha-client>`_ which is included in the package as ``client.py``.

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

#. Add the Google reCAPTCHA keys generated in step 1 to your Django production settings. Note that omitting these settings will default to a set of test keys which can be used for development.``RECAPTCHA_PUBLIC_KEY`` and ``RECAPTCHA_PRIVATE_KEY``. Also ensure ``SILENCED_SYSTEM_CHECKS = [..., 'captcha.recaptcha_test_key_error', ...]`` is set to bypass the security check that prevents the test keys from being used unknowingly.

    For example:

    .. code-block:: python

        RECAPTCHA_PUBLIC_KEY = 'MyRecaptchaKey123'
        RECAPTCHA_PRIVATE_KEY = 'MyRecaptchaPrivateKey456'

    These can also be specified per field by passing the ``public_key`` or
    ``private_key`` parameters to ``ReCaptchaField`` - see field usage below.

#. (OPTIONAL) If you require a proxy, add a ``RECAPTCHA_PROXY`` setting (dictionary of proxies), for example:

    .. code-block:: python

        RECAPTCHA_PROXY = {'http': 'http://127.0.0.1:8000', 'https': 'https://127.0.0.1:8000'}

#. (OPTIONAL) In the event ``www.google.com`` is not accessible the ``RECAPTCHA_DOMAIN`` setting can be changed to ``www.recaptcha.net`` as per the `reCAPTCHA FAQ <https://developers.google.com/recaptcha/docs/faq#can-i-use-recaptcha-globally>`_:

    .. code-block:: python

        RECAPTCHA_DOMAIN = 'www.recaptcha.net'

This will change the Google JavaScript api domain as well as the client side field verification domain.

Usage
-----

Fields
~~~~~~

The quickest way to add reCAPTCHA to a form is to use the included
``ReCaptchaField`` field class. A ``ReCaptchaV2Checkbox`` will be rendered by default. For example:

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

If specified, these parameters will be used instead of your reCAPTCHA project settings.

Widgets
~~~~~~~

There are three widgets that can be used with the ``ReCaptchaField`` class:

    ``ReCaptchaV2Checkbox`` for `Google reCAPTCHA V2 - Checkbox <https://developers.google.com/recaptcha/docs/display>`_

    ``ReCaptchaV2Invisible`` for `Google reCAPTCHA V2 - Invisible <https://developers.google.com/recaptcha/docs/invisible>`_

    ``ReCaptchaV3`` for `Google reCAPTCHA V3 <https://developers.google.com/recaptcha/docs/v3>`_

To make use of widgets other than the default Google reCAPTCHA V2 - Checkbox widget, simply replace the ``ReCaptchaField`` widget. For example:

.. code-block:: python

    from django import forms
    from captcha.fields import ReCaptchaField
    from captcha.widgets import ReCaptchaV2Invisible

    class FormWithCaptcha(forms.Form):
        captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

The reCAPTCHA widget supports several `data attributes
<https://developers.google.com/recaptcha/docs/display#render_param>`_ that
customize the behaviour of the widget, such as ``data-theme``, ``data-size``, etc. You can
forward these options to the widget by passing an ``attrs`` parameter to the
widget, containing a dictionary of options. For example:

.. code-block:: python

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

The reCAPTCHA api supports several `paramaters
<https://developers.google.com/recaptcha/docs/display#js_param>`_. To customise
the paramaters that get sent along pass an ``api_params`` paramater to the
widget, containing a dictionary of options. For example:

.. code-block:: python

    captcha = fields.ReCaptchaField(
        widget=widgets.ReCaptchaV2Checkbox(
            api_params={'hl': 'cl', 'onload': 'onLoadFunc'}
        )
    )
    # The dictionary is urlencoded and appended to the reCAPTCHA api url.

By default, the widgets provided only supports a single form with a single widget on each page.

The language can be set with the 'h1' parameter, look at `language codes
<https://developers.google.com/recaptcha/docs/language>`_ for the language code options. Note that translations need to be added to this package for the errors to be shown correctly. Currently the package has error translations for the following language codes: es, fr, nl, pl, pt_BR, ru, zh_CN, zh_TW

However, the JavaScript used by the widgets can easily be overridden in the templates.

The templates are located in:

    ``captcha/includes/js_v2_checkbox.html`` for overriding the reCAPTCHA V2 - Checkbox template

    ``captcha/includes/js_v2_invisible.html`` for overriding the reCAPTCHA V2 - Invisible template

    ``captcha/includes/js_v3.html`` for overriding the reCAPTCHA V3 template

 For more information about overriding templates look at `Django's template override <https://docs.djangoproject.com/en/2.1/howto/overriding-templates/>`_

Local Development and Functional Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Google provides test keys which are set as the default for ``RECAPTCHA_PUBLIC_KEY`` and ``RECAPTCHA_PRIVATE_KEY``. These cannot be used in production since they always validate to true and a warning will be shown on the reCAPTCHA.


Credits
-------
Inspired Marco Fucci's blogpost titled `Integrating reCAPTCHA with Django
<http://www.marcofucci.com/tumblelog/26/jul/2009/integrating-recaptcha-with-django>`_


``client.py`` taken from `recaptcha-client
<http://pypi.python.org/pypi/recaptcha-client>`_ licenced MIT/X11 by Mike
Crawford.

reCAPTCHA copyright 2012 Google.
