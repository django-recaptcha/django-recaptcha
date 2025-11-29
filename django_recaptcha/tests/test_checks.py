from django.test import TestCase, override_settings

from django_recaptcha.checks import recaptcha_key_check
from django_recaptcha.constants import TEST_PRIVATE_KEY


def _filter_errs(errs, err_id):
    """Returns filtered list with relevant error."""
    return [e for e in errs if e.id == err_id]


class TestChecks(TestCase):

    @override_settings(RECAPTCHA_PRIVATE_KEY="notempty")
    def test_check_private_key_is_empty_passes(self):
        errs = recaptcha_key_check("someconf")
        errs = _filter_errs(errs, "django_recaptcha.private_key_is_empty_string")

        self.assertEqual(0, len(errs))

    @override_settings(RECAPTCHA_PRIVATE_KEY="")
    def test_check_private_key_is_empty_fails(self):
        errs = recaptcha_key_check("someconf")
        errs = _filter_errs(errs, "django_recaptcha.private_key_is_empty_string")

        self.assertEqual(1, len(errs))

    @override_settings(RECAPTCHA_PUBLIC_KEY="notempty")
    def test_check_public_key_is_empty_passes(self):
        errs = recaptcha_key_check("someconf")
        errs = _filter_errs(errs, "django_recaptcha.public_key_is_empty_string")

        self.assertEqual(0, len(errs))

    @override_settings(RECAPTCHA_PUBLIC_KEY="")
    def test_check_public_key_is_empty_fails(self):
        errs = recaptcha_key_check("someconf")
        errs = _filter_errs(errs, "django_recaptcha.public_key_is_empty_string")

        self.assertEqual(1, len(errs))

    @override_settings(DEBUG=True, RECAPTCHA_PRIVATE_KEY=TEST_PRIVATE_KEY)
    def test_check_test_key_usage_skipped(self):
        errs = recaptcha_key_check("someconf")
        errs = _filter_errs(errs, "django_recaptcha.recaptcha_test_key_error")

        self.assertEqual(0, len(errs))

    @override_settings(
        DEBUG=False,
        RECAPTCHA_PRIVATE_KEY="privatekey",
        RECAPTCHA_PUBLIC_KEY="publickey",
    )
    def test_check_test_key_usage_passes(self):
        errs = recaptcha_key_check("someconf")
        errs = _filter_errs(errs, "django_recaptcha.recaptcha_test_key_error")

        self.assertEqual(0, len(errs))

    @override_settings(DEBUG=False, RECAPTCHA_PRIVATE_KEY=TEST_PRIVATE_KEY)
    def test_check_test_key_usage_fails(self):
        errs = recaptcha_key_check("someconf")
        errs = _filter_errs(errs, "django_recaptcha.recaptcha_test_key_error")

        self.assertEqual(1, len(errs))
