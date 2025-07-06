import json
from unittest.mock import patch

from django.test import TestCase, override_settings

import django_recaptcha.enterprise.client as m

from . import fixtures as f


class AssessmentTests(TestCase):
    """Tests Assessment class."""

    def test_access_data_directly(self):
        """Should be able to access response data directly."""
        response_data = f.create_response_data()

        assessment = m.Assessment(response_data)
        result = assessment.data

        self.assertEqual(result, response_data)

    def test_is_token_valid(self):
        """Should assert token's validity correctly."""

        # This test matrix is based on the following parameters:
        # 1. is token valid? yes/no
        # 2. is token action specified? yes/no
        # 3. is expected action specified? yes/no
        # 4. if both (2) and (3) are specified, do they match? yes/no
        test_matrix = [
            ((True, "login", "login"), True),
            ((True, "login", "logout"), False),
            ((True, "login", ""), False),
            ((True, "", "login"), False),
            ((True, "", ""), True),
            ((False, "login", "login"), False),
            ((False, "login", "logout"), False),
            ((False, "login", ""), False),
            ((False, "", "login"), False),
            ((False, "", ""), False),
        ]

        for (valid, token_action, expected_action), expected in test_matrix:
            response_data = f.create_response_data(
                valid=valid, token_action=token_action, expected_action=expected_action
            )

            assessment = m.Assessment(response_data)
            result = assessment.is_token_valid()

            self.assertEqual(result, expected)

    def test_is_token_valid__missing_data(self):
        """Should raise exception if needed data is missing."""
        response_data = f.create_response_data()
        del response_data["tokenProperties"]["valid"]

        assessment = m.Assessment(response_data)
        with self.assertRaises(m.MissingAssessmentData) as exc:
            _ = assessment.is_token_valid()

        self.assertEqual(
            str(exc.exception),
            "Object with key 'valid' is missing from assessment data.",
        )

    def test_score(self):
        """Should return the assessment's score correctly."""
        response_data = f.create_response_data(score=0.3)

        assessment = m.Assessment(response_data)
        result = assessment.score

        self.assertEqual(result, 0.3)

    def test_score__missing_data(self):
        """Should raise exception if needed data is missing."""
        response_data = f.create_response_data()
        del response_data["riskAnalysis"]["score"]

        assessment = m.Assessment(response_data)
        with self.assertRaises(m.MissingAssessmentData) as exc:
            _ = assessment.score

        self.assertEqual(
            str(exc.exception),
            "Object with key 'score' is missing from assessment data.",
        )


class CreateAssessmentTests(TestCase):
    """Tests create_assessment() function."""

    @patch("django_recaptcha.enterprise.client.send_request")
    def test_create_assessment(self, send_request_mock):
        """Should send request data and return response data as expected."""
        request_data = f.create_request_data()
        response_data = f.create_response_data(valid=True)
        send_request_mock.return_value = response_data

        assessment = m.create_assessment(
            project_id=f.PROJECT_ID,
            site_key=f.SITEKEY,
            access_token=f.ACCESS_TOKEN,
            recaptcha_token=f.RECAPTCHA_TOKEN,
        )

        send_request_mock.assert_called_once_with(
            f"https://recaptchaenterprise.googleapis.com/v1/projects/{f.PROJECT_ID}/assessments",
            f.ACCESS_TOKEN,
            request_data,
        )
        self.assertEqual(assessment.data, response_data)

    @patch("django_recaptcha.enterprise.client.send_request")
    def test_create_assessment__include_action(self, send_request_mock):
        """Should include expected action in request data if specified."""
        request_data = f.create_request_data(action="login")

        _ = m.create_assessment(
            project_id=f.PROJECT_ID,
            site_key=f.SITEKEY,
            access_token=f.ACCESS_TOKEN,
            recaptcha_token=f.RECAPTCHA_TOKEN,
            expected_action="login",
        )

        send_request_mock.assert_called_once_with(
            f"https://recaptchaenterprise.googleapis.com/v1/projects/{f.PROJECT_ID}/assessments",
            f.ACCESS_TOKEN,
            request_data,
        )

    @patch("django_recaptcha.enterprise.client.send_request")
    def test_create_assessment__include_requested_uri(self, send_request_mock):
        """Should include requested URI in request data if specified."""
        request_data = f.create_request_data(requested_uri="https://example.com/")

        _ = m.create_assessment(
            project_id=f.PROJECT_ID,
            site_key=f.SITEKEY,
            access_token=f.ACCESS_TOKEN,
            recaptcha_token=f.RECAPTCHA_TOKEN,
            requested_uri="https://example.com/",
        )

        send_request_mock.assert_called_once_with(
            f"https://recaptchaenterprise.googleapis.com/v1/projects/{f.PROJECT_ID}/assessments",
            f.ACCESS_TOKEN,
            request_data,
        )

    @patch("django_recaptcha.enterprise.client.send_request")
    def test_create_assessment__include_user_agent(self, send_request_mock):
        """Should include user agent in request data if specified."""
        request_data = f.create_request_data(user_agent="my-user-agent")

        _ = m.create_assessment(
            project_id=f.PROJECT_ID,
            site_key=f.SITEKEY,
            access_token=f.ACCESS_TOKEN,
            recaptcha_token=f.RECAPTCHA_TOKEN,
            user_agent="my-user-agent",
        )

        send_request_mock.assert_called_once_with(
            f"https://recaptchaenterprise.googleapis.com/v1/projects/{f.PROJECT_ID}/assessments",
            f.ACCESS_TOKEN,
            request_data,
        )

    @patch("django_recaptcha.enterprise.client.send_request")
    def test_create_assessment__include_ip_address(self, send_request_mock):
        """Should include user's IP address in request data if specified."""
        request_data = f.create_request_data(user_ip_address="1.2.3.4")

        _ = m.create_assessment(
            project_id=f.PROJECT_ID,
            site_key=f.SITEKEY,
            access_token=f.ACCESS_TOKEN,
            recaptcha_token=f.RECAPTCHA_TOKEN,
            user_ip_address="1.2.3.4",
        )

        send_request_mock.assert_called_once_with(
            f"https://recaptchaenterprise.googleapis.com/v1/projects/{f.PROJECT_ID}/assessments",
            f.ACCESS_TOKEN,
            request_data,
        )

    @patch("django_recaptcha.enterprise.client.send_request")
    def test_create_assessment__api_call_failed(self, send_request_mock):
        """Should re-raise exception if API call fails with an added note."""
        send_request_mock.side_effect = m.ReCAPTCHAEnterpriseAPICallFailed()

        with self.assertRaises(m.ReCAPTCHAEnterpriseAPICallFailed) as exc:
            _ = m.create_assessment(
                project_id=f.PROJECT_ID,
                site_key=f.SITEKEY,
                access_token=f.ACCESS_TOKEN,
                recaptcha_token=f.RECAPTCHA_TOKEN,
            )

        self.assertEqual(
            exc.exception.__notes__, ["failed during call: projects.assessments.create"]
        )


class SendRequestTests(TestCase):
    """Tests send_request() function."""

    @patch("django_recaptcha.enterprise.client.Request")
    @patch("django_recaptcha.enterprise.client.ProxyHandler")
    @patch("django_recaptcha.enterprise.client.build_opener")
    def test_send_request(self, build_opener_mock, proxy_handler_mock, request_mock):
        """Should send request data and return response data as expected."""
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

        result = m.send_request("<URL>", "<ACCESS_TOKEN>", request_data)

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
        self.assertEqual(result, response_data)

    @patch("django_recaptcha.enterprise.client.Request")
    @patch("django_recaptcha.enterprise.client.ProxyHandler")
    @patch("django_recaptcha.enterprise.client.build_opener")
    @override_settings(RECAPTCHA_ENTERPRISE_PROXY={"http": "<HTTP_PROXY>"})
    def test_send_request__use_proxy(
        self, build_opener_mock, proxy_handler_mock, request_mock
    ):
        """Should use a proxy if specified."""
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
    def test_send_request__use_different_timeout(
        self, build_opener_mock, proxy_handler_mock, request_mock
    ):
        """Should use a different timeout if specfied."""
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

    @patch("django_recaptcha.enterprise.client.Request")
    @patch("django_recaptcha.enterprise.client.ProxyHandler")
    @patch("django_recaptcha.enterprise.client.build_opener")
    def test_send_request__api_call_failed(
        self, build_opener_mock, proxy_handler_mock, request_mock
    ):
        """Should raise an exception if the API call fails unexpectedly."""
        request_data = f.create_request_data()

        # opener = ...
        opener_obj_mock = build_opener_mock.return_value
        opener_obj_mock.open.side_effect = m.URLError("")

        with self.assertRaises(m.ReCAPTCHAEnterpriseAPICallFailed) as exc:
            _ = m.send_request("<URL>", "<ACCESS_TOKEN>", request_data)

        self.assertEqual(str(exc.exception), "API call failed.")
