import uuid

try:
    from unittest.mock import patch, PropertyMock, MagicMock
except ImportError:
    from mock import patch, PropertyMock, MagicMock

from django.test import TestCase
from django.conf import settings

from captcha import client, constants


class TestClient(TestCase):

    @patch("captcha.client.recaptcha_request")
    def test_client_success(self, mocked_response):
        read_mock = MagicMock()
        read_mock.read.return_value = b'{"success": true, "challenge_ts":' \
            b'"2019-01-11T13:57:23Z", "hostname": "testkey.google.com"}'
        mocked_response.return_value = read_mock
        uuid_hex = uuid.uuid4().hex
        response = client.submit(
            uuid_hex,
            "somekey",
            "0.0.0.0",
        )

        # Quick way to test method call without needing to worry about Python 2
        # dicts not being ordered by default.
        self.assertIn("secret=somekey", mocked_response.call_args.__str__())
        self.assertIn(
            "response=%s" % uuid_hex, mocked_response.call_args.__str__()
        )
        self.assertIn("remoteip=0.0.0.0", mocked_response.call_args.__str__())
        self.assertTrue(response.is_valid)

    @patch("captcha.client.recaptcha_request")
    def test_client_success(self, mocked_response):
        read_mock = MagicMock()
        read_mock.read.return_value = b'{"success": false, "error-codes":' \
            b'["invalid-input-response", "invalid-input-secret"]}'
        mocked_response.return_value = read_mock
        uuid_hex = uuid.uuid4().hex
        response = client.submit(
            uuid_hex,
            "somekey",
            "0.0.0.0",
        )

        # Quick way to test method call without needing to worry about Python 2
        # dicts not being ordered by default.
        self.assertIn("secret=somekey", mocked_response.call_args.__str__())
        self.assertIn(
            "response=%s" % uuid_hex, mocked_response.call_args.__str__()
        )
        self.assertIn("remoteip=0.0.0.0", mocked_response.call_args.__str__())
        self.assertFalse(response.is_valid)
        self.assertEqual(
            response.error_codes.sort(),
            ["invalid-input-response", "invalid-input-secret"].sort()
        )
