Django reCAPTCHA
================
**Django reCAPTCHA form field/widget integration app.**

.. contents:: Contents
    :depth: 5

Installation
------------

#. Install or add ``django-recaptcha`` to your Python path.

Usage
-----

django-registration
~~~~~~~~~~~~~~~~~~~
django-recaptcha ships with a `django-registration <https://bitbucket.org/ubernostrum/django-registration>`_ backend extending the default backend to include a reCAPTCHA field. This is included mostly as an example of how you could intergrate a reCAPTCHA field with django-registration. I suggest you familiarize yourself with `the django-registration docs <http://docs.b-list.org/django-registration/0.8/index.html>`_ for more comprehensive documentation. 

To use the reCAPTHCA backend complete these steps:

#. Add captcha registration backend url include to your project's ``urls.py`` file::

    (r'^accounts/', include('captcha.backends.default.urls')),

#. Add an ``ACCOUNT_ACTIVATION_DAYS`` setting to the project's ``settings.py`` file. This is the number of days users will have to activate their accounts after registering, as required by django-registration, i.e.::
    
    ACCOUNT_ACTIVATION_DAYS = 7

#. Implement various `templates as required by django-registration <http://docs.b-list.org/django-registration/0.8/quickstart.html#required-templates>`_.

Once done you should be able to access `/accounts/register/ <http://localhost:8000/accounts/register/>`_ and see reCAPTCHA in action.

Credits
-------
Inspired Marco Fucci's blogpost titled `Integrating reCAPTCHA with Django <http://www.marcofucci.com/tumblelog/26/jul/2009/integrating-recaptcha-with-django>`_
reCAPTCHA © 2011 Google

