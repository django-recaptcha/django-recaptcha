import os
import unittest

from captcha import fields
from django.forms import Form


class TestForm(Form):
    captcha = fields.ReCaptchaField(attrs={'theme': 'white'})

class TestCase(unittest.TestCase):

    def setUp(self):
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def test_envvar_enabled(self):
        form_params = {'recaptcha_response_field': 'PASSED'}
        form = TestForm(form_params)
        self.assertTrue(form.is_valid())

    def test_envvar_disabled(self):
        os.environ['RECAPTCHA_TESTING'] = 'False'
        form_params = {'recaptcha_response_field': 'PASSED'}
        form = TestForm(form_params)
        self.assertFalse(form.is_valid())

    def tearDown(self):
        del os.environ['RECAPTCHA_TESTING']
