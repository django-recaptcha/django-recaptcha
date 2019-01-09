Changelog
=========

1.5.0 (2019-01-09)
------------------

#. Added testing for Django 2.1 (no code changes needed).
#. Update the unit tests to no longer make use of reCAPTCHA v1.
#. Added deprecation warnings for reCAPTCHA v1 support.
#. Remove the need for RECAPTCHA_TESTING environment variable during unit testing.
#. Added Invisible reCAPTCHA V2 support.

1.4.0 (2018-02-08)
------------------

#. Dropped support for Django < 1.11.
#. Added testing for Django 2.0 (no code changes needed).

1.3.1 (2017-06-27)
------------------

#. Fixed widget attributes regression for Django < 1.10.

1.3.0 (2017-04-10)
------------------

#. Support Django 1.11 in addition to 1.8, 1.9, and 1.10.


1.2.1 (2017-01-23)
------------------

#. Made reCAPTCHA test keys the default keys for easy use in development. The
   captcha doesn't require any interaction, has a warning label that it's for
   testing purposes only, and always validates.

1.2.0 (2016-12-19)
------------------

#. Pass options as HTML data attributes instead of the ``RecaptchaOptions``
   JavaScript object in the default template. Custom templates using
   ``RecaptchaOptions`` should migrate to using HTML data attributes.

1.1.0 (2016-10-28)
------------------

#. Dropped support for old Django versions. Only the upstream supported
   versions are now supported, currently 1.8, 1.9, and 1.10.
#. Made recaptcha checking use SSL by default. This can be disabled by setting
   ``RECAPTCHA_USE_SSL = False`` in your Django settings or passing
   ``use_ssl=False`` to the constructor of ``ReCaptchaField``.
#. Made ReCaptchaField respect required=False

1.0.6 (2016-10-05)
------------------

#. Confirmed tests pass on Django 1.10. Older versions should still work.
#. Fixed a bug where the widget was always rendered in the first used language
   due to ``attrs`` being a mutable default argument.

1.0.5 (2016-01-04)
------------------
#. Chinese translation (kz26).
#. Syntax fix (zvin).
#. Get tests to pass on Django 1.9.

1.0.4 (2015-04-16)
------------------
#. Fixed Python 3 support
#. Added Polish translations
#. Update docs

1.0.3 (2015-01-13)
------------------
#. Added nocaptcha recaptcha support

1.0.2 (2014-09-16)
------------------
#. Fixed Russian translations
#. Added Spanish translations

1.0.1 (2014-09-11)
------------------
#. Added Django 1.7 suport
#. Added Russian translations
#. Added multi dependancy support
#. Cleanup

1.0 (2014-04-23)
----------------
#. Added Python 3 support
#. Added French, Dutch and Brazilian Portuguese translations

0.0.9 (2014-02-14)
------------------
#. Bugfix: release master and not develop. This should fix the confusion due to master having been the default branch on Github.

0.0.8 (2014-02-13)
------------------
#. Bugfix: remove reference to options.html.

0.0.7 (2014-02-12)
------------------
#. Make it possible to load the widget via ajax.

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
