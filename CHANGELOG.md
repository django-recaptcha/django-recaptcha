# Changelog

## 4.1.0 [Unreleased]

- The GitHub project has been transferred to [django-recaptcha/django-recaptcha](https://github.com/django-recaptcha/django-recaptcha), to facilitate maintenance by the community.
  See the [maintainers discussion in GitHub](https://github.com/orgs/django-recaptcha/discussions/249).
- Removed: the undocumented `django_recaptcha.client.RECAPTCHA_SUPPORTED_LANGUAGES` constant was removed as it serves no purpose ([#342](https://github.com/django-recaptcha/django-recaptcha/pull/342))
- Added: Persian translations ([#326](https://github.com/django-recaptcha/django-recaptcha/pull/326))
- Fixed: removed unnecessary `type="text/javascript"` from all script tags ([#324](https://github.com/django-recaptcha/django-recaptcha/pull/324))
- Fixed: `ReCaptchaV2Invisible` and `ReCaptchaV2Checkbox` widgets no longer render unnecessary labels, improving accessibility ([#328](https://github.com/django-recaptcha/django-recaptcha/pull/328))
- Fixed: `ReCaptchaV2Invisible` and `ReCaptchaV2Checkbox` widgets no longer render a `required` attribute on the container div because this is not a valid attribute on this element ([#328](https://github.com/django-recaptcha/django-recaptcha/pull/328))
- Deprecated: passing `required_score` as part of RecaptchaV3 widget `attrs` is deprecated to avoid rendering `required_score` as a HTML attribute ([#330](https://github.com/django-recaptcha/django-recaptcha/pull/330))
- Maintenance: made tox Django version specifiers more specific ([#339](https://github.com/django-recaptcha/django-recaptcha/pull/339))

### Upgrade considerations

#### Passing `required_score` as part of RecaptchaV3 widget `attrs` is deprecated

Passing `required_score` as part of RecaptchaV3 widget `attrs` is deprecated and will raise a deprecation warning. You should pass `required_score` as a keyword argument to the RecaptchaV3 widget instead. Support for passing `required_score` as part of RecaptchaV3 widget `attrs` will be removed in the next major release.

Example of how you should update your code:

```diff
# Old
- ReCaptchaV3(attrs={"required_score": 0.5})
# New
+ ReCaptchaV3(required_score=0.5)
```

This change was made to avoid rendering `required_score` as a HTML attribute. This is important because `required_score` is not a valid HTML attribute and is often flagged as such by HTML validators.

## 4.0.0 (2023-11-14)

> [!IMPORTANT] > **BREAKING**: package namespace renamed from `captcha` to `django_recaptcha`. See upgrade considerations section below for instructions ([#317](https://github.com/django-recaptcha/django-recaptcha/pull/317))

- Removed: support for Django 4.0 and 2.2
- Removed: support for Python 3.7
- Added: support for Django 4.1 and 4.2
- Added: support for Python 3.11
- Added: support for the `action` parameter in the ReCaptchaV3 widget ([#304](https://github.com/django-recaptcha/django-recaptcha/pull/304), [#309](https://github.com/django-recaptcha/django-recaptcha/pull/309) and [#310](https://github.com/django-recaptcha/django-recaptcha/pull/310))
- Added: Arabic translations ([#313](https://github.com/django-recaptcha/django-recaptcha/pull/313))
- Added: Indonesian translations ([#301](https://github.com/django-recaptcha/django-recaptcha/pull/301))
- Added: Ukrainian translations ([#315](https://github.com/django-recaptcha/django-recaptcha/pull/315))
- Fixed: don't display a form field label when using the ReCaptchaV3 widget as it is invisible ([#294](https://github.com/django-recaptcha/django-recaptcha/pull/294))
- Fixed: execute ReCaptcha V3 validation on form submit instead of on page load to avoid captcha errors if the form takes more than 2 minutes to complete ([#296](https://github.com/django-recaptcha/django-recaptcha/pull/296))
- Fixed: avoid outputting duplicate `class` attribute in widget html when a custom `class` attribute is passed to the widget ([#275](https://github.com/django-recaptcha/django-recaptcha/pull/275))
- Docs: update testing instructions ([#300](https://github.com/django-recaptcha/django-recaptcha/pull/300))
- Docs: add example unittest for `RECAPTCHA_TESTING` ([#289](https://github.com/django-recaptcha/django-recaptcha/pull/289))

### Upgrade considerations from v3 to v4

#### Package namespace renamed

The package namespace has been renamed from `captcha` to `django_recaptcha` to avoid namespace conflicts with other captcha packages. This means that you will need to update your imports and `INSTALLED_APPS` setting.

**Action required:** update your imports like this:

```diff
# Old
-from captcha.fields import ReCaptchaField
-from captcha.widgets import ReCaptchaV2Checkbox, ReCaptchaV2Invisible, ReCaptchaV3
# New
+from django_recaptcha.fields import ReCaptchaField
+from django_recaptcha.widgets import ReCaptchaV2Checkbox, ReCaptchaV2Invisible, ReCaptchaV3
```

**Action required:** update your Django settings like this:

```diff
INSTALLED_APPS = [
    # ...
    # Old
-    "captcha",
    # New
+    "django_recaptcha",
    # ...
]
```

#### ReCaptchaV3 widget no longer supplies a default action to the ReCaptcha API

[Google's reCAPTCHA V3 API supports passing an action value](https://developers.google.com/recaptcha/docs/v3#actions).
Actions allow you to tie reCAPTCHA validations to a specific form on your site for analytical purposes, enabling you to perform risk analysis per form. This will allow you to make informed decisions about adjusting the score threshold for certain forms because abusive behavior can vary depending on the nature of the form.

Previously, the `ReCaptchaV3` widget used a hardcoded value for the `action` parameter which was not configurable. This meant that all ReCaptcha V3 validations for your site were tied to the same action: `form`, defeating the purpose of actions.

Starting with v4.0.0, the `ReCaptchaV3` widget now takes an `action` argument. If you don't supply this argument no action will be passed to the reCAPTCHA V3 API. Passing an action is optional, but recommended.

**Optional:** consider passing an `action` argument to the `ReCaptchaV3` widget.

Example:

```python
class ContactForm(forms.Form):
    # All captcha validations for this form will be tied to the "contact_form" action.
    # You can view the validation statistics in the reCAPTCHA admin console.
    captcha = ReCaptchaField(widget=ReCaptchaV3(action="contact_form"))
```

#### ReCaptchaV3 widget no longer displays a label

Previously, the `RecaptchaV3` widget displayed a label which was confusing as ReCaptcha validation is done in the background and the widget is invisible. This redundant label has been removed in v4.0.0. If you previously removed the label yourself by passing `label=""` to `RecaptchaField` you can now remove this argument.

## 3.0.0 (2022-02-07)

- Individual contributors supported by Torchbox have taken over maintenance of this package from Praekelt.
  See the [Github Announcement](https://github.com/orgs/django-recaptcha/discussions/249)
- Switch testing from Travis to Github Actions.
- Only provide default_app_config for django.VERSIONs lower than 3.2
- Changed log level of check failures from error to warning.
- Added testing for Django 3.2 and 4.0
- Removed support for Django 1.11 and Python 2
- Removed upper Django dependency constraint

## 2.0.6

- Added testing for Django 3 (no code changes needed).

## 2.0.5

- Added settings and kwargs that allow for the validation of reCAPTCHA
  v3 score values.

## 2.0.4

- Fixed travis tests for django 2.2

## 2.0.3

- Added testing for Django 2.2 (no code changes needed).

## 2.0.2

- Moved field based Google dev key check to an app ready registered
  security check.

## 2.0.1

- Bugfix: Remove extra div in widget_v3 template

## 2.0.0

- ReCAPTCHA v3 support added.
- Remove all mention of the V1 reCAPTCHA endpoint.
- Refactor client, fields and widgets code.
- Added widgets for each type of reCAPTCHA: `V2 Checkbox`,
  `V2 Invisible`, `V3`
- Remove the need for the widget template to be selected based on
  certain settings values, each widget has its own template.
- Introduced a large number of new unit tests, update tests to make
  use of tox venvs.
- Regenerated po and mo files.

## 1.5.0 (2019-01-09)

- Added testing for Django 2.1 (no code changes needed).
- Update the unit tests to no longer make use of reCAPTCHA v1.
- Added deprecation warnings for reCAPTCHA v1 support.
- Remove the need for RECAPTCHA_TESTING environment variable during
  unit testing.
- Added Invisible reCAPTCHA V2 support.

## 1.4.0 (2018-02-08)

- Dropped support for Django \< 1.11.
- Added testing for Django 2.0 (no code changes needed).

## 1.3.1 (2017-06-27)

- Fixed widget attributes regression for Django \< 1.10.

## 1.3.0 (2017-04-10)

- Support Django 1.11 in addition to 1.8, 1.9, and 1.10.

## 1.2.1 (2017-01-23)

- Made reCAPTCHA test keys the default keys for easy use in
  development. The captcha doesn't require any interaction, has a
  warning label that it's for testing purposes only, and always
  validates.

## 1.2.0 (2016-12-19)

- Pass options as HTML data attributes instead of the
  `RecaptchaOptions` JavaScript object in the default template. Custom
  templates using `RecaptchaOptions` should migrate to using HTML data
  attributes.

## 1.1.0 (2016-10-28)

- Dropped support for old Django versions. Only the upstream supported
  versions are now supported, currently 1.8, 1.9, and 1.10.
- Made recaptcha checking use SSL by default. This can be disabled by
  setting `RECAPTCHA_USE_SSL = False` in your Django settings or
  passing `use_ssl=False` to the constructor of `ReCaptchaField`.
- Made ReCaptchaField respect required=False

## 1.0.6 (2016-10-05)

- Confirmed tests pass on Django 1.10. Older versions should still
  work.
- Fixed a bug where the widget was always rendered in the first used
  language due to `attrs` being a mutable default argument.

## 1.0.5 (2016-01-04)

- Chinese translation (kz26).
- Syntax fix (zvin).
- Get tests to pass on Django 1.9.

## 1.0.4 (2015-04-16)

- Fixed Python 3 support
- Added Polish translations
- Update docs

## 1.0.3 (2015-01-13)

- Added nocaptcha recaptcha support

## 1.0.2 (2014-09-16)

- Fixed Russian translations
- Added Spanish translations

## 1.0.1 (2014-09-11)

- Added Django 1.7 support
- Added Russian translations
- Added multi dependency support
- Cleanup

## 1.0 (2014-04-23)

- Added Python 3 support
- Added French, Dutch and Brazilian Portuguese translations

## 0.0.9 (2014-02-14)

- Bugfix: release master and not develop. This should fix the
  confusion due to master having been the default branch on Github.

## 0.0.8 (2014-02-13)

- Bugfix: remove reference to options.html.

## 0.0.7 (2014-02-12)

- Make it possible to load the widget via ajax.

## 0.0.6 (2013-01-31)

- Added an extra parameter <span class="title-ref">lang</span> to
  bypass Google's language bug. See
  <http://code.google.com/p/recaptcha/issues/detail?id=133#c3>
- widget.html no longer includes options.html. Options are added
  directly to widget.html

## 0.0.5 (2013-01-17)

- Removed django-registration dependency
- Changed testing mechanism to environmental variable
  <span class="title-ref">RECAPTCHA_TESTING</span>

## 0.0.4

- Handle missing REMOTE_ADDR request meta key. Thanks Joe Jasinski.
- Added checks for settings.DEBUG to facilitate tests. Thanks Victor
  Neo.
- Fix for correct iframe URL in case of no javascript. Thanks gerdemb.

## 0.0.3 (2011-09-20)

- Don't force registration version thanks kshileev.
- Render widget using template, thanks denz.

## 0.0.2 (2011-08-10)

- Use remote IP when validating.
- Added SSL support, thanks Brooks Travis.
- Added support for Javascript reCAPTCHA widget options, thanks
  Brandon Taylor.
- Allow for key and ssl specification at runtime, thanks Evgeny
  Fadeev.

## 0.0.1 (2010-06-17)

- Initial release.
