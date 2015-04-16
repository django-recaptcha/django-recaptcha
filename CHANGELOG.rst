Changelog
=========

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
