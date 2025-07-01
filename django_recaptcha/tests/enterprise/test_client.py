import json
from unittest.mock import patch

from django.test import TestCase, override_settings

import django_recaptcha.enterprise.client as m

from . import fixtures as f


class VerificationResultTests(TestCase):
    """Tests VerificationResult class."""

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

        self.assertTrue(result.is_okay(0.0))

    def test_is_okay__invalid_token(self):
        """Invalid token are not okay."""
        response_data = f.create_response_data(valid=False)

        result = m.VerificationResult(response_data)

        self.assertFalse(result.is_okay(0.0))

    def test_is_okay__actions_set_and_matching(self):
        """Token is okay if token's action matches expectation."""
        response_data = f.create_response_data(
            client_action="login", expected_action="login"
        )

        result = m.VerificationResult(response_data)

        self.assertTrue(result.is_okay(0.0))

    def test_is_okay__actions_set_and_not_matching(self):
        """Token is not okay if token's action doesn't match expectation."""
        response_data = f.create_response_data(
            client_action="login", expected_action="pay"
        )

        result = m.VerificationResult(response_data)

        self.assertFalse(result.is_okay(0.0))

    def test_is_okay__only_client_action_set(self):
        """Token is not okay if token has unexpected associated action."""
        response_data = f.create_response_data(client_action="login")

        result = m.VerificationResult(response_data)

        self.assertFalse(result.is_okay(0.0))

    def test_is_okay__only_server_action_set(self):
        """Token is not okay if token lacks the expected associated action."""
        response_data = f.create_response_data(expected_action="login")

        result = m.VerificationResult(response_data)

        self.assertFalse(result.is_okay(0.0))

    def test_is_okay__score_higher_than_required(self):
        """Token is okay if its score is higher than required."""
        response_data = f.create_response_data(score=0.9)

        result = m.VerificationResult(response_data)

        self.assertTrue(result.is_okay(0.5))

    def test_is_okay__score_equal_to_required_score(self):
        """Token is okay if its score is equal to the required score."""
        response_data = f.create_response_data(score=0.5)

        result = m.VerificationResult(response_data)

        self.assertTrue(result.is_okay(0.5))

    def test_is_okay__score_lower_than_required(self):
        """Token is not okay if its score is lower than required."""
        response_data = f.create_response_data(score=0.1)

        result = m.VerificationResult(response_data)

        self.assertFalse(result.is_okay(0.5))

    def test_get_score(self):
        """Can retrieve the score correctly."""
        response_data = f.create_response_data(score=0.3)

        result = m.VerificationResult(response_data)

        self.assertEqual(result.score, 0.3)


class VerifyEnterpriseV1TokenTests(TestCase):

    @patch("django_recaptcha.enterprise.client.send_request")
    def test_success(self, send_mock):
        """Request data is submitted and response data returned as expected."""
        request_data = f.create_request_data()
        response_data = f.create_response_data(valid=True)

        send_mock.return_value = response_data

        verification_result = m.verify_enterprise_v1_token(
            project_id="alpha-beta-123",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
            recaptcha_token=f.RECAPTCHA_TOKEN,
        )

        send_mock.assert_called_once_with(
            "https://recaptchaenterprise.googleapis.com/v1/projects/alpha-beta-123/assessments",
            "<ACCESS-TOKEN>",
            request_data,
        )
        self.assertEqual(verification_result.data, response_data)

    @patch("django_recaptcha.enterprise.client.send_request")
    def test_submit_token_with_action(self, send_mock):
        """Expected action is submitted if action is specified."""
        request_data = f.create_request_data(action="myaction")

        _ = m.verify_enterprise_v1_token(
            project_id="alpha-beta-123",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
            recaptcha_token=f.RECAPTCHA_TOKEN,
            expected_action="myaction",
        )

        send_mock.assert_called_once_with(
            "https://recaptchaenterprise.googleapis.com/v1/projects/alpha-beta-123/assessments",
            "<ACCESS-TOKEN>",
            request_data,
        )

    @patch("django_recaptcha.enterprise.client.send_request")
    def test_submit_requested_uri(self, send_mock):
        """Requested URI is submitted if specified."""
        request_data = f.create_request_data(requested_uri="https://example.com/")

        _ = m.verify_enterprise_v1_token(
            project_id="alpha-beta-123",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
            recaptcha_token=f.RECAPTCHA_TOKEN,
            requested_uri="https://example.com/",
        )

        send_mock.assert_called_once_with(
            "https://recaptchaenterprise.googleapis.com/v1/projects/alpha-beta-123/assessments",
            "<ACCESS-TOKEN>",
            request_data,
        )

    @patch("django_recaptcha.enterprise.client.send_request")
    def test_submit_user_agent(self, send_mock):
        """User agent is submitted if specified."""
        request_data = f.create_request_data(user_agent="my-user-agent")

        _ = m.verify_enterprise_v1_token(
            project_id="alpha-beta-123",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
            recaptcha_token=f.RECAPTCHA_TOKEN,
            user_agent="my-user-agent",
        )

        send_mock.assert_called_once_with(
            "https://recaptchaenterprise.googleapis.com/v1/projects/alpha-beta-123/assessments",
            "<ACCESS-TOKEN>",
            request_data,
        )

    @patch("django_recaptcha.enterprise.client.send_request")
    def test_submit_user_ip_address(self, send_mock):
        """User IP address is submitted if specified."""
        request_data = f.create_request_data(user_ip_address="1.2.3.4")

        _ = m.verify_enterprise_v1_token(
            project_id="alpha-beta-123",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
            recaptcha_token=f.RECAPTCHA_TOKEN,
            user_ip_address="1.2.3.4",
        )

        send_mock.assert_called_once_with(
            "https://recaptchaenterprise.googleapis.com/v1/projects/alpha-beta-123/assessments",
            "<ACCESS-TOKEN>",
            request_data,
        )


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
            method="POST",
        )
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
    @override_settings(RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT=5.0)
    def test_different_timeout(
        self, build_opener_mock, proxy_handler_mock, request_mock
    ):
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
