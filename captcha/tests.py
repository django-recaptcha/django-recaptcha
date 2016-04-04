import os
import unittest

from captcha import fields
from django.forms import Form
from django.test.utils import override_settings


class TestForm(Form):
    captcha = fields.ReCaptchaField(attrs={'theme': 'white'})


class TestCase(unittest.TestCase):

    @override_settings(RECAPTCHA_TESTING=True)
    def test_envvar_enabled(self):
        form_params = {'recaptcha_response_field': 'PASSED'}
        form = TestForm(form_params)
        self.assertTrue(form.is_valid())

    @override_settings(RECAPTCHA_TESTING=False)
    def test_envvar_disabled(self):
        form_params = {'recaptcha_response_field': 'PASSED'}
        form = TestForm(form_params)
        self.assertFalse(form.is_valid())
