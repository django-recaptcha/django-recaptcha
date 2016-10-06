Django reCAPTCHA
================
**Django reCAPTCHA form field/widget integration app.**

.. image:: https://travis-ci.org/praekelt/django-recaptcha.svg?branch=develop
    :target: https://travis-ci.org/praekelt/django-recaptcha

.. contents:: Contents
    :depth: 5

django-recaptcha uses a modified version of the `Python reCAPTCHA client <http://pypi.python.org/pypi/recaptcha-client>`_ which is included in the package as ``client.py``.


Requirements
------------

Tested with:

* Python: 2.7, 3.5
* Django: 1.8, 1.9, 1.10

Installation
------------

#. Install or add ``django-recaptcha`` to your Python path.

#. Add ``captcha`` to your ``INSTALLED_APPS`` setting.

#. Add a ``RECAPTCHA_PUBLIC_KEY`` setting to the project's ``settings.py`` file. This is your public API key as provided by reCAPTCHA, i.e.:

   .. code-block:: python

       RECAPTCHA_PUBLIC_KEY = '76wtgdfsjhsydt7r5FFGFhgsdfytd656sad75fgh'

   This can be seperately specified at runtime by passing a ``public_key`` parameter when constructing the ``ReCaptchaField``, see field usage below.

#. Add a ``RECAPTCHA_PRIVATE_KEY`` setting to the project's ``settings.py`` file. This is your private API key as provided by reCAPTCHA, i.e.:

   .. code-block:: python

       RECAPTCHA_PRIVATE_KEY = '98dfg6df7g56df6gdfgdfg65JHJH656565GFGFGs'

   This can be seperately specified at runtime by passing a ``private_key`` parameter when constructing the ``ReCaptchaField``, see field usage below.

#. If you would like to use the new No Captcha reCaptcha add a ``NOCAPTCHA = True`` setting to the project's ``settings.py`` file. ie.:

   .. code-block:: python

       NOCAPTCHA = True

#. Optionally add a ``RECAPTCHA_USE_SSL`` setting to the project's ``settings.py`` file. This causes reCAPTCHA validation submits to be made over SSL, i.e.:

   .. code-block:: python

       RECAPTCHA_USE_SSL = True

   If you don't add this setting the default behaviour is to **NOT** use SSL. Note that if you have ``NOCAPTCHA = True`` set, SSL will always be used.
   This can be seperately specified at runtime by passing a ``use_ssl`` parameter when constructing the ``ReCaptchaField``, see field usage below.

#. If you require a proxy, add a ``RECAPTCHA_PROXY`` setting to the project's ``settings.py`` file, i.e.:

   .. code-block:: python

       RECAPTCHA_PROXY = 'http://127.0.0.1:8000'

Usage
-----

Field
~~~~~
The quickest way to add reCAPTCHA to a form is to use the included ``ReCaptchaField`` field class. A ``ReCaptcha`` widget will be rendered with the field validating itself without any further action required from you. For example:

.. code-block:: python

    from django import forms
    from captcha.fields import ReCaptchaField

    class FormWithCaptcha(forms.Form):
        captcha = ReCaptchaField()

To allow for runtime specification of keys and SSL usage you can optionally pass the ``private_key``, ``public_key``, or ``use_ssl`` parameters to the constructor. For example:

.. code-block:: python

    captcha = ReCaptchaField(
        public_key='76wtgdfsjhsydt7r5FFGFhgsdfytd656sad75fgh',
        private_key='98dfg6df7g56df6gdfgdfg65JHJH656565GFGFGs',
        use_ssl=True,
    )

If specified these parameters will be used instead of your reCAPTCHA project settings.

The reCAPTCHA widget supports several `Javascript options variables <https://developers.google.com/recaptcha/docs/display#js_param>`_ customizing the behaviour of the widget, such as ``theme`` and ``lang``. You can forward these options to the widget by passing an ``attr`` parameter containing a dictionary of options to ``ReCaptchaField``. For example:

.. code-block:: python

    captcha = ReCaptchaField(attrs={'theme' : 'clean'})

The captcha client takes the key/value pairs and writes out the RecaptchaOptions value in JavaScript.


Unit Testing
~~~~~~~~~~~~

django-recaptcha introduces an environmental variable ``RECAPTCHA_TESTING`` which
helps facilitate tests. The environmental variable should be set to ``"True"``,
and cleared, using the ``setUp()`` and ``tearDown()`` methods in your test classes.

Setting ``RECAPTCHA_TESTING`` to ``True`` causes django-recaptcha to accept
``"PASSED"`` as the ``recaptcha_response_field`` value. Note that if you are using the new No Captcha reCaptcha
(ie. with ``NOCAPTCHA = True`` in your settings) the response field is called ``g-recaptcha-response``.

Example:

.. code-block:: python

    import os
    os.environ['RECAPTCHA_TESTING'] = 'True'

    form_params = {'recaptcha_response_field': 'PASSED'} # use 'g-recaptcha-response' param name if using NOCAPTCHA
    form = RegistrationForm(form_params) # assuming only one ReCaptchaField
    form.is_valid() # True

    os.environ['RECAPTCHA_TESTING'] = 'False'
    form.is_valid() # False

Passing any other values will cause django-recaptcha to continue normal processing
and return a form error.

Check ``tests.py`` for a full example.


AJAX
~~~~~

To make Recapcha work in ajax-loaded forms:

#. Import ``recaptcha_ajax.js`` on your page (not in the loaded template):

   .. code-block:: html

       <script type="text/javascript" src="http://www.google.com/recaptcha/api/js/recaptcha_ajax.js"></script>

#. Add to your Django settings:

   .. code-block:: python


       CAPTCHA_AJAX = True


Credits
-------
Inspired Marco Fucci's blogpost titled `Integrating reCAPTCHA with Django <http://www.marcofucci.com/tumblelog/26/jul/2009/integrating-recaptcha-with-django>`_


``client.py`` taken from `recaptcha-client <http://pypi.python.org/pypi/recaptcha-client>`_ licenced MIT/X11 by Mike Crawford.

reCAPTCHA copyright 2012 Google.
