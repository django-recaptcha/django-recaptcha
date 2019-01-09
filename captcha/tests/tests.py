import os
import warnings

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from captcha import fields
from django.forms import Form
from django.test import TestCase, override_settings

from captcha.client import RecaptchaResponse


class TestForm(Form):
    captcha = fields.ReCaptchaField(attrs={'theme': 'white'})


class TestCase(TestCase):
    @patch("captcha.fields.client.submit")
    def test_client_success_response(self, mocked_submit):
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        form_params = {'g-recaptcha-response': 'PASSED'}
        form = TestForm(form_params)
        self.assertTrue(form.is_valid())

    @patch("captcha.fields.client.submit")
    def test_client_failure_response(self, mocked_submit):
        mocked_submit.return_value = RecaptchaResponse(is_valid=False, error_code="410")
        form_params = {'g-recaptcha-response': 'PASSED'}
        form = TestForm(form_params)
        self.assertFalse(form.is_valid())

    def test_client_integration(self):
       form_params = {'g-recaptcha-response': 'PASSED'}
       form = TestForm(form_params)

       # Trigger client.submit
       form.is_valid()
