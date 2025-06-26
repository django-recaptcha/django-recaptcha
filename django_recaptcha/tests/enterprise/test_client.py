import json
from unittest.mock import patch, MagicMock

from django.test import TestCase, override_settings

import django_recaptcha.enterprise.client as m

from . import fixtures as f


class VerificationResultTests(TestCase):

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


class VerifyEnterpriseV1TokenTests(TestCase):

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


class SendRequestTests(TestCase):

    @patch("django_recaptcha.enterprise.client.Request")
    @patch("django_recaptcha.enterprise.client.ProxyHandler")
    @patch("django_recaptcha.enterprise.client.build_opener")
    def test_success(self, build_opener_mock, proxy_handler_mock, request_mock):
        request_data = f.create_request_data()
        request_data_bytes = json.dumps(request_data).encode("utf-8")
        response_data = f.create_response_data()
        response_data_bytes = json.dumps(response_data).encode("utf-8")

        # request = ...
        request_obj_mock = request_mock.return_value

        # opener = ...
        opener_obj_mock = build_opener_mock.return_value

        # response = ...
        response_obj_mock = opener_obj_mock.open.return_value
        response_obj_mock.read.return_value = response_data_bytes

        returned_data = m.send_request("<URL>", "<ACCESS_TOKEN>", request_data)

        request_mock.assert_called_once_with(
            url="<URL>",
            data=request_data_bytes,
            headers={
                "X-goog-api-key": "<ACCESS_TOKEN>",
                "Content-Type": "application/json; charset=utf-8",
            },
            method="POST")
        proxy_handler_mock.assert_not_called()
        build_opener_mock.assert_called_once_with()
        opener_obj_mock.open.assert_called_once_with(request_obj_mock, timeout=10.0)
        response_obj_mock.read.assert_called_once()
        self.assertEqual(returned_data, response_data)


    @patch("django_recaptcha.enterprise.client.Request")
    @patch("django_recaptcha.enterprise.client.ProxyHandler")
    @patch("django_recaptcha.enterprise.client.build_opener")
    @override_settings(RECAPTCHA_ENTERPRISE_PROXY={"http": "<HTTP_PROXY>"})
    def test_use_proxy(self, build_opener_mock, proxy_handler_mock, request_mock):
        """Can use setting to use proxies."""
        request_data = f.create_request_data()
        response_data = f.create_response_data()
        response_data_bytes = json.dumps(response_data).encode("utf-8")

        # opener = ...
        opener_obj_mock = build_opener_mock.return_value

        # response = ...
        response_obj_mock = opener_obj_mock.open.return_value
        response_obj_mock.read.return_value = response_data_bytes

        _ = m.send_request("<URL>", "<ACCESS_TOKEN>", request_data)

        proxy_handler_mock.assert_called_once_with({"http": "<HTTP_PROXY>"})
        build_opener_mock.assert_called_once_with(proxy_handler_mock.return_value)

    @patch("django_recaptcha.enterprise.client.Request")
    @patch("django_recaptcha.enterprise.client.ProxyHandler")
    @patch("django_recaptcha.enterprise.client.build_opener")
    @override_settings(RECAPTCHA_ENTERPRISE_TIMEOUT=5.0)
    def test_different_timeout(self, build_opener_mock, proxy_handler_mock, request_mock):
        """Can use setting to change timeout."""
        request_data = f.create_request_data()
        response_data = f.create_response_data()
        response_data_bytes = json.dumps(response_data).encode("utf-8")

        # request = ...
        request_obj_mock = request_mock.return_value

        # opener = ...
        opener_obj_mock = build_opener_mock.return_value

        # response = ...
        response_obj_mock = opener_obj_mock.open.return_value
        response_obj_mock.read.return_value = response_data_bytes

        _ = m.send_request("<URL>", "<ACCESS_TOKEN>", request_data)

        opener_obj_mock.open.assert_called_once_with(request_obj_mock, timeout=5.0)
