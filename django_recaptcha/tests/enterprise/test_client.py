import json
from unittest.mock import patch, MagicMock

from django.test import TestCase

import django_recaptcha.enterprise.client as m

from . import fixtures as f


class VerificationResultTest(TestCase):

    def test_access_data_directly(self):
        """User should be able to access data directly for convenience."""
        response_data = f.create_response_data()

        result = m.VerificationResult(response_data)

        self.assertEqual(result.data["event"]["token"], f.RECAPTCHA_TOKEN)
        self.assertEqual(result.data["tokenProperties"]["valid"], True)

    def test_is_okay__valid_token(self):
        """Valid token are okay."""
        response_data = f.create_response_data(valid=True)

        result = m.VerificationResult(response_data)

        self.assertTrue(result.is_okay())

    def test_is_okay__invalid_token(self):
        """Invalid token are not okay."""
        response_data = f.create_response_data(valid=False)

        result = m.VerificationResult(response_data)

        self.assertFalse(result.is_okay())


class TestVerifyEnterpriseV1Token(TestCase):

    @patch("django_recaptcha.enterprise.client.send_request")
    def test_success__valid_token(self, send_mock):
        request_data = f.create_request_data()
        response_data = f.create_response_data(valid=True)

        send_mock.return_value = response_data

        verification_result = m.verify_enterprise_v1_token(
            project_id="alpha-beta-123",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
            recaptcha_token=f.RECAPTCHA_TOKEN)

        send_mock.assert_called_once_with(
            "https://recaptchaenterprise.googleapis.com/v1/projects/alpha-beta-123/assessments",
            "<ACCESS-TOKEN>",
            request_data,
        )
        self.assertEqual(verification_result.data, response_data)

    @patch("django_recaptcha.enterprise.client.send_request")
    def test_success__invalid_token(self, send_mock):
        request_data = f.create_request_data()
        response_data = f.create_response_data(valid=False)

        send_mock.return_value = response_data

        verification_result = m.verify_enterprise_v1_token(
            project_id="alpha-beta-123",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
            recaptcha_token=f.RECAPTCHA_TOKEN)

        send_mock.assert_called_once_with(
            "https://recaptchaenterprise.googleapis.com/v1/projects/alpha-beta-123/assessments",
            "<ACCESS-TOKEN>",
            request_data,
        )
        self.assertEqual(verification_result.data, response_data)
