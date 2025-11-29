from django.test import TestCase, override_settings

from django.core.checks import Error
import django_recaptcha
from django_recaptcha.constants import TEST_PRIVATE_KEY


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
        DEBUG=False,
        RECAPTCHA_PRIVATE_KEY=TEST_PRIVATE_KEY,
    )
    def test_check_test_key_usage_fails(self):
        errs = django_recaptcha.checks.recaptcha_key_check("someconf")
        relevant_errs = [e for e in errs if e.id == "django_recaptcha.recaptcha_test_key_error"]

        self.assertEqual(1, len(relevant_errs))
