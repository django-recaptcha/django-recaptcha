from django.test import TestCase, override_settings

from django_recaptcha.enterprise.conf import use_setting


class UseSettingTests(TestCase):
    """Tests use_setting() function."""

    @override_settings(RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT=30.0)
    def test__use_argument(self):
        """Use argument even if value is also set by Django settings."""
        result = use_setting("RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT", 20.0)
        self.assertEqual(result, 20.0)

    @override_settings(RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT=30.0)
    def test__use_django_setting(self):
        """Should use value set by Django setting if argument is not provided."""
        result = use_setting("RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT")
        self.assertEqual(result, 30.0)

    def test__use_default_setting(self):
        """Should use default value if no argument or Django setting is provided."""
        result = use_setting("RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT")
        self.assertEqual(result, 10.0)
