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

NOTE:
-----

As of March 2018 the reCAPTCHA v1 Google endpoints no longer exist.
Currently django-recaptcha still makes use of those endpoints when either
``CAPTCHA_AJAX = True`` or ``NOCAPTCHA = False``. To make use of the default reCAPTCHA v2
checkbox, please ensure ``NOCAPTCHA = True`` and ``CAPTCHA_AJAX`` is not present in
your project settings.
Moving forward, this project will be removing the lingering reCAPTCHA v1 and
the need to add ``NOCAPTCHA = True`` for reCAPTCHA v2 support.

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

#. Add the keys reCAPTCHA have given you to your Django production settings (leave development settings blank to use the default test keys) as
   ``RECAPTCHA_PUBLIC_KEY`` and ``RECAPTCHA_PRIVATE_KEY``. For example:

   .. code-block:: python

       RECAPTCHA_PUBLIC_KEY = 'MyRecaptchaKey123'
       RECAPTCHA_PRIVATE_KEY = 'MyRecaptchaPrivateKey456'

   These can also be specificied per field by passing the ``public_key`` or
   ``private_key`` parameters to ``ReCaptchaField`` - see field usage below.

#. To ensure the reCAPTCHA V2 endpoints are used add the setting:

   .. code-block:: python

       NOCAPTCHA = True # Marked for deprecation in version 2.0

#. To make use of the invisible reCAPTCHA V2, ensure ``NOCAPTCHA = True`` is present in your settings and then also dd:

   .. code-block:: python

       RECAPTCHA_V2_INVISIBLE = True # Marked for deprecation in version 2.0

Out of the box the invisible implementation only supports one form with the reCAPTCHA widget on a page. This widget must be wrapped in a form element.
To alter the JavaScript behaviour to suit your project needs, override ``captcha/includes/js_v2_invisible.html`` in your local project template directory.

#. If you require a proxy, add a ``RECAPTCHA_PROXY`` setting, for example:

   .. code-block:: python

       RECAPTCHA_PROXY = 'http://127.0.0.1:8000'

Usage
-----

Field
~~~~~

The quickest way to add reCAPTCHA to a form is to use the included
``ReCaptchaField`` field class. A ``ReCaptcha`` widget will be rendered with
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

If specified these parameters will be used instead of your reCAPTCHA project
settings.

The reCAPTCHA widget supports several `Javascript options variables
<https://developers.google.com/recaptcha/docs/display#js_param>`_ that
customize the behaviour of the widget, such as ``theme`` and ``lang``. You can
forward these options to the widget by passing an ``attr`` parameter to the
field, containing a dictionary of options. For example:

.. code-block:: python

    captcha = ReCaptchaField(attrs={
      'theme' : 'clean',
    })

The client takes the key/value pairs and writes out the ``RecaptchaOptions``
value in JavaScript.


Local Development and Functional Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Google provides test keys which are set as the default for ``RECAPTCHA_PUBLIC_KEY`` and ``RECAPTCHA_PRIVATE_KEY``. These cannot be used in production since they always validate to true and a warning will be shown on the reCAPTCHA.


AJAX(Marked for deprecation in version 2.0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To make reCAPTCHA work in ajax-loaded forms:

#. Import ``recaptcha_ajax.js`` on your page (not in the loaded template):

   .. code-block:: html

       <script type="text/javascript" src="http://www.google.com/recaptcha/api/js/recaptcha_ajax.js"></script>

#. Add to your Django settings:

   .. code-block:: python

       CAPTCHA_AJAX = True


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
