Changelog
=========

0.0.6 (2013-01-31)
------------------
#. Added an extra parameter `lang` to bypass Google's language bug. See http://code.google.com/p/recaptcha/issues/detail?id=133#c3
#. widget.html no longer includes options.html. Options are added directly to widget.html

0.0.5 (2013-01-17)
------------------
#. Removed django-registration dependency
#. Changed testing mechanism to environmental variable `RECAPTCHA_TESTING`

0.0.4
-----
#. Handle missing REMOTE_ADDR request meta key. Thanks Joe Jasinski.
#. Added checks for settings.DEBUG to facilitate tests. Thanks Victor Neo.
#. Fix for correct iframe URL in case of no javascript. Thanks gerdemb.

0.0.3 (2011-09-20)
------------------
#. Don't force registration version thanks kshileev.
#. Render widget using template, thanks denz.

0.0.2 (2011-08-10)
------------------
#. Use remote IP when validating.
#. Added SSL support, thanks Brooks Travis.
#. Added support for Javascript reCAPTCHA widget options, thanks Brandon Taylor.
#. Allow for key and ssl specification at runtime, thanks Evgeny Fadeev.

0.0.1 (2010-06-17)
------------------
#. Initial release.

