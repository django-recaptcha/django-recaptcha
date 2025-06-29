from django.test import TestCase, override_settings

from django_recaptcha.enterprise.conf import use_setting


class UseSettingTests(TestCase):
    """Tests the ``use_setting()`` function."""

    @override_settings(RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT=30.0)
    def test__use_argument(self):
        """Use argument even if value is also set by django settings."""
        result = use_setting("RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT", 20.0)
        self.assertEqual(result, 20.0)

    @override_settings(RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT=30.0)
    def test__use_django_setting(self):
        """Use value set by django settings if argument is not provided."""
        result = use_setting("RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT", None)
        self.assertEqual(result, 30.0)

    def test__use_default_setting(self):
        """Use default value if no argument or django setting is provided."""
        result = use_setting("RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT", None)
        self.assertEqual(result, 10.0)
