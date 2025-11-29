from django.test import TestCase, override_settings

from django.core.checks import Error
import django_recaptcha


class TestChecks(TestCase):

    @override_settings(RECAPTCHA_PRIVATE_KEY="notempty")
    def test_check_private_key_is_empty_passes(self):
        errs = django_recaptcha.checks.recaptcha_key_check("someconf")
        relevant_errs = [e for e in errs if e.id == "django_recaptcha.private_key_is_empty_string"]

        self.assertEqual(0, len(relevant_errs))

    @override_settings(RECAPTCHA_PRIVATE_KEY="")
    def test_check_private_key_is_empty_fails(self):
        errs = django_recaptcha.checks.recaptcha_key_check("someconf")
        relevant_errs = [e for e in errs if e.id == "django_recaptcha.private_key_is_empty_string"]

        self.assertEqual(1, len(relevant_errs))

    @override_settings(RECAPTCHA_PUBLIC_KEY="notempty")
    def test_check_public_key_is_empty_passes(self):
        errs = django_recaptcha.checks.recaptcha_key_check("someconf")
        relevant_errs = [e for e in errs if e.id == "django_recaptcha.public_key_is_empty_string"]

        self.assertEqual(0, len(relevant_errs))

    @override_settings(RECAPTCHA_PUBLIC_KEY="")
    def test_check_public_key_is_empty_fails(self):
        errs = django_recaptcha.checks.recaptcha_key_check("someconf")
        relevant_errs = [e for e in errs if e.id == "django_recaptcha.public_key_is_empty_string"]

        self.assertEqual(1, len(relevant_errs))

    @override_settings(
        RECAPTCHA_PRIVATE_KEY=django_recaptcha.constants.TEST_PRIVATE_KEY
    )
    def test_test_key_check(self):
        check_errors = django_recaptcha.checks.recaptcha_key_check("someconf")
        expected_errors = [
            Error(
                "RECAPTCHA_PRIVATE_KEY or RECAPTCHA_PUBLIC_KEY is making use"
                " of the Google test keys and will not behave as expected in a"
                " production environment",
                hint="Update settings.RECAPTCHA_PRIVATE_KEY"
                " and/or settings.RECAPTCHA_PUBLIC_KEY. Alternatively this"
                " check can be ignored by adding"
                " `SILENCED_SYSTEM_CHECKS ="
                " ['django_recaptcha.recaptcha_test_key_error']`"
                " to your settings file.",
                id="django_recaptcha.recaptcha_test_key_error",
            )
        ]
        self.assertEqual(check_errors, expected_errors)
