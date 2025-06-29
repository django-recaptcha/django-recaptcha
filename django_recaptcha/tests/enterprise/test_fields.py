from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.test import TestCase

from django_recaptcha.enterprise.client import VerificationResult
from django_recaptcha.enterprise.fields import ReCAPTCHAEnterpriseV1CheckboxField

from . import fixtures as f


class ReCAPTCHAEnterpriseV1CheckboxFieldTests(TestCase):
    """Tests the ReCAPTCHAEnterpriseV1CheckboxField class."""

    def test_init__bad_action_name(self):
        """An exception should be raised if the ... ."""
        with self.assertRaises(ImproperlyConfigured) as e:
            _ = ReCAPTCHAEnterpriseV1CheckboxField(
                project_id="<PROJECT-ID>",
                sitekey=f.SITEKEY,
                access_token="<ACCESS-TOKEN>",
                action="not-valid",  # cannot contain -
            )

        self.assertEqual(
            str(e.exception), "Action 'not-valid' contains disallowed character(s)."
        )

    @patch("django_recaptcha.enterprise.fields.verify_enterprise_v1_token")
    def test_validate__value_not_provided(self, verify_mock):
        """Validation should fail if Field class' validation fails."""
        captcha_field = ReCAPTCHAEnterpriseV1CheckboxField(
            project_id="<PROJECT-ID>", sitekey=f.SITEKEY, access_token="<ACCESS-TOKEN>"
        )

        # fails because fields are required by default
        with self.assertRaises(ValidationError) as e:
            captcha_field.validate(None)

        self.assertEqual(e.exception.code, "required")
        verify_mock.assert_not_called()

    @patch("django_recaptcha.enterprise.fields.verify_enterprise_v1_token")
    def test_validate__good_token(self, verify_mock):
        """Validation should pass if nothing is wrong with token."""
        captcha_field = ReCAPTCHAEnterpriseV1CheckboxField(
            project_id="<PROJECT-ID>", sitekey=f.SITEKEY, access_token="<ACCESS-TOKEN>"
        )
        response_data = f.create_response_data(valid=True)
        verify_mock.return_value = VerificationResult(response_data)

        captcha_field.validate(f.RECAPTCHA_TOKEN)

        verify_mock.assert_called_once_with(
            "<PROJECT-ID>", f.SITEKEY, "<ACCESS-TOKEN>", f.RECAPTCHA_TOKEN, None
        )

    @patch("django_recaptcha.enterprise.fields.verify_enterprise_v1_token")
    def test_validate__bad_token(self, verify_mock):
        """Validation should fail if token is invalid."""
        captcha_field = ReCAPTCHAEnterpriseV1CheckboxField(
            project_id="<PROJECT-ID>", sitekey=f.SITEKEY, access_token="<ACCESS-TOKEN>"
        )
        response_data = f.create_response_data(valid=False)
        verify_mock.return_value = VerificationResult(response_data)

        with self.assertRaises(ValidationError) as e:
            captcha_field.validate(f.RECAPTCHA_TOKEN)

        self.assertEqual(e.exception.code, "captcha_invalid")
        verify_mock.assert_called_once_with(
            "<PROJECT-ID>", f.SITEKEY, "<ACCESS-TOKEN>", f.RECAPTCHA_TOKEN, None
        )

    @patch("django_recaptcha.enterprise.fields.verify_enterprise_v1_token")
    def test_validate__action_is_passed_along(self, verify_mock):
        """Validation"""
        captcha_field = ReCAPTCHAEnterpriseV1CheckboxField(
            project_id="<PROJECT-ID>",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
            action="ACTION",
        )
        response_data = f.create_response_data(
            client_action="ACTION", expected_action="ACTION"
        )
        verify_mock.return_value = VerificationResult(response_data)

        captcha_field.validate(f.RECAPTCHA_TOKEN)

        verify_mock.assert_called_once_with(
            "<PROJECT-ID>", f.SITEKEY, "<ACCESS-TOKEN>", f.RECAPTCHA_TOKEN, "ACTION"
        )
