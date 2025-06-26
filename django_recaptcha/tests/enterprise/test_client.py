from django.test import TestCase

import django_recaptcha.enterprise.client as m

from . import fixtures as f


class VerificationResultTest(TestCase):

    def test_access_data_directly(self):
        """User should be able to access data directly for convenience."""
        response_data = f.create_response()

        result = m.VerificationResult(response_data)

        self.assertEqual(result.data["event"]["token"], f.RECAPTCHA_TOKEN)
        self.assertEqual(result.data["tokenProperties"]["valid"], True)

    def test_is_okay__valid_token(self):
        """Valid token are okay."""
        response_data = f.create_response(valid=True)

        result = m.VerificationResult(response_data)

        self.assertTrue(result.is_okay())

    def test_is_okay__invalid_token(self):
        """Invalid token are not okay."""
        response_data = f.create_response(valid=False)

        result = m.VerificationResult(response_data)

        self.assertFalse(result.is_okay())
