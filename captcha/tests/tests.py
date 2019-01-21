try:
    from importlib import reload
except ImportError:
    pass

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

import captcha


class TestInit(TestCase):

    def test_setting_instance_check(self):
        with override_settings(RECAPTCHA_PROXY="not a dict"):
            with self.assertRaises(ImproperlyConfigured) as error:
                reload(captcha)
            self.assertEqual(error.exception.args, (
                "Setting RECAPTCHA_PROXY is not of type", dict)
            )
        with override_settings(RECAPTCHA_VERIFY_REQUEST_TIMEOUT="not an int"):
            with self.assertRaises(ImproperlyConfigured) as error:
                reload(captcha)
            self.assertEqual(error.exception.args, (
                "Setting RECAPTCHA_VERIFY_REQUEST_TIMEOUT is not of type", int)
            )
        with override_settings(RECAPTCHA_DOMAIN=1):
            with self.assertRaises(ImproperlyConfigured) as error:
                reload(captcha)
            self.assertEqual(error.exception.args, (
                "Setting RECAPTCHA_DOMAIN is not of type", str)
            )
        with override_settings(RECAPTCHA_PUBLIC_KEY=1):
            with self.assertRaises(ImproperlyConfigured) as error:
                reload(captcha)
            self.assertEqual(error.exception.args, (
                "Setting RECAPTCHA_PUBLIC_KEY is not of type", str)
            )
        with override_settings(RECAPTCHA_PRIVATE_KEY=1):
            with self.assertRaises(ImproperlyConfigured) as error:
                reload(captcha)
            self.assertEqual(error.exception.args, (
                "Setting RECAPTCHA_PRIVATE_KEY is not of type", str)
            )
