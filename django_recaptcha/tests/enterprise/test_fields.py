from unittest.mock import MagicMock, patch

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.forms.widgets import TextInput
from django.test import TestCase, override_settings

from django_recaptcha.enterprise.client import VerificationResult
from django_recaptcha.enterprise.fields import ReCAPTCHAEnterpriseV1Field
from django_recaptcha.enterprise.widgets import ReCAPTCHAEnterpriseNoHTMLWidget

from . import fixtures as f


class ReCAPTCHAEnterpriseV1FieldTests(TestCase):
    """Tests the ReCAPTCHAEnterpriseV1Field class."""

    def test_init__project_id_not_provided(self):
        """Raise exception if no value is set for project_id."""
        with self.assertRaises(ImproperlyConfigured) as e:
            _ = ReCAPTCHAEnterpriseV1Field(
                sitekey=f.SITEKEY,
                access_token="ACCESS-TOKEN",
            )

        self.assertEqual(
            str(e.exception),
            "Must provide value of project_id as an argument or Django setting.",
        )

    @override_settings(RECAPTCHA_ENTERPRISE_PROJECT_ID="<PROJECT-ID>")
    def test_init__project_id_provided_as_django_setting(self):
        """Use Django setting to set value for project_id."""
        captcha = ReCAPTCHAEnterpriseV1Field(
            sitekey=f.SITEKEY,
            access_token="ACCESS-TOKEN",
        )

        self.assertEqual(captcha._project_id, "<PROJECT-ID>")

    def test_init__sitekey_not_provided(self):
        """Raise exception if no value is set for sitekey."""
        with self.assertRaises(ImproperlyConfigured) as e:
            _ = ReCAPTCHAEnterpriseV1Field(
                project_id="<PROJECT-ID>",
                access_token="<ACCESS-TOKEN>",
            )

        self.assertEqual(
            str(e.exception),
            "Must provide value of sitekey as an argument or Django setting.",
        )

    @override_settings(RECAPTCHA_ENTERPRISE_SITEKEY=f.SITEKEY)
    def test_init__sitekey_provided_as_django_setting(self):
        """Use Django setting to set value for sitekey."""
        _ = ReCAPTCHAEnterpriseV1Field(
            project_id="<PROJECT-ID>",
            access_token="<ACCESS-TOKEN>",
        )

    def test_init__access_token_not_provided(self):
        """Raise exception if no value is set for access_token."""
        with self.assertRaises(ImproperlyConfigured) as e:
            _ = ReCAPTCHAEnterpriseV1Field(
                project_id="<PROJECT-ID>",
                sitekey=f.SITEKEY,
            )

        self.assertEqual(
            str(e.exception),
            "Must provide value of access_token as an argument or Django setting.",
        )

    @override_settings(RECAPTCHA_ENTERPRISE_ACCESS_TOKEN="<ACCESS-TOKEN>")
    def test_init__access_token_provided_as_django_setting(self):
        """Use Django setting to set value for access_token."""
        _ = ReCAPTCHAEnterpriseV1Field(
            project_id="<PROJECT-ID>",
            sitekey=f.SITEKEY,
        )

    def test_init__bad_action_name(self):
        """Raise exception if action name contains a disallowed character."""
        with self.assertRaises(ImproperlyConfigured) as e:
            _ = ReCAPTCHAEnterpriseV1Field(
                project_id="<PROJECT-ID>",
                sitekey=f.SITEKEY,
                access_token="<ACCESS-TOKEN>",
                action="not-valid",  # cannot contain -
            )

        self.assertEqual(
            str(e.exception), "Action 'not-valid' contains disallowed character(s)."
        )

    def test_init__bad_widget_type(self):
        """Raise exception if widget is not an instance of the right type."""
        with self.assertRaises(TypeError) as e:
            _ = ReCAPTCHAEnterpriseV1Field(
                project_id="<PROJECT-ID>",
                sitekey=f.SITEKEY,
                access_token="<ACCESS-TOKEN>",
                widget=TextInput(),
            )

        self.assertEqual(
            str(e.exception), "Widget must be an instance of ReCAPTCHAEnterpriseWidget."
        )

    def test_init__set_sitekey_on_widget(self):
        """Should call set_sitekey() on widget."""
        widget = ReCAPTCHAEnterpriseNoHTMLWidget()
        widget.set_sitekey = MagicMock()

        _ = ReCAPTCHAEnterpriseV1Field(
            project_id="<PROJECT-ID>",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
            widget=widget,
        )

        widget.set_sitekey.assert_called_once_with(f.SITEKEY)

    def test_init__dont_set_action_on_widget(self):
        """Should not call set_action() on widget if action is not specified."""
        widget = ReCAPTCHAEnterpriseNoHTMLWidget()
        widget.set_action = MagicMock()

        _ = ReCAPTCHAEnterpriseV1Field(
            project_id="<PROJECT-ID>",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
            widget=widget,
        )

        widget.set_action.assert_not_called()

    def test_init__set_action_on_widget(self):
        """Should call set_action() on widget if action is specified."""
        widget = ReCAPTCHAEnterpriseNoHTMLWidget()
        widget.set_action = MagicMock()

        _ = ReCAPTCHAEnterpriseV1Field(
            project_id="<PROJECT-ID>",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
            widget=widget,
            action="login",
        )

        widget.set_action.assert_called_once_with("login")

    @patch("django_recaptcha.enterprise.fields.verify_enterprise_v1_token")
    def test_validate__value_not_provided(self, verify_mock):
        """Validation should fail if Field class' validation fails."""
        captcha_field = ReCAPTCHAEnterpriseV1Field(
            project_id="<PROJECT-ID>",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
        )

        # fails because fields are required by default
        with self.assertRaises(ValidationError) as e:
            captcha_field.validate(None)

        self.assertEqual(e.exception.code, "required")
        verify_mock.assert_not_called()

    @patch("django_recaptcha.enterprise.fields.verify_enterprise_v1_token")
    def test_validate__good_token(self, verify_mock):
        """Validation should pass if nothing is wrong with token."""
        captcha_field = ReCAPTCHAEnterpriseV1Field(
            project_id="<PROJECT-ID>",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
        )
        response_data = f.create_response_data(valid=True)
        verify_mock.return_value = VerificationResult(response_data)

        captcha_field.validate(f.RECAPTCHA_TOKEN)

        verify_mock.assert_called_once_with(
            "<PROJECT-ID>",
            f.SITEKEY,
            "<ACCESS-TOKEN>",
            f.RECAPTCHA_TOKEN,
            None,
            None,
            None,
            None,
        )

    @patch("django_recaptcha.enterprise.fields.verify_enterprise_v1_token")
    def test_validate__bad_token(self, verify_mock):
        """Validation should fail if token is invalid."""
        captcha_field = ReCAPTCHAEnterpriseV1Field(
            project_id="<PROJECT-ID>",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
        )
        response_data = f.create_response_data(valid=False)
        verify_mock.return_value = VerificationResult(response_data)

        with self.assertRaises(ValidationError) as e:
            captcha_field.validate(f.RECAPTCHA_TOKEN)

        self.assertEqual(e.exception.code, "captcha_invalid")
        verify_mock.assert_called_once_with(
            "<PROJECT-ID>",
            f.SITEKEY,
            "<ACCESS-TOKEN>",
            f.RECAPTCHA_TOKEN,
            None,
            None,
            None,
            None,
        )

    @patch("django_recaptcha.enterprise.fields.verify_enterprise_v1_token")
    def test_validate__action_is_passed_along(self, verify_mock):
        """Validation should include action if passed along."""
        captcha_field = ReCAPTCHAEnterpriseV1Field(
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
            "<PROJECT-ID>",
            f.SITEKEY,
            "<ACCESS-TOKEN>",
            f.RECAPTCHA_TOKEN,
            "ACTION",
            None,
            None,
            None,
        )

    @patch("django_recaptcha.enterprise.fields.verify_enterprise_v1_token")
    def test_validate__score_is_set_after_validation(self, verify_mock):
        """Score should be set after validation."""
        captcha_field = ReCAPTCHAEnterpriseV1Field(
            project_id="<PROJECT-ID>",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
        )
        response_data = f.create_response_data(score=0.7)
        verify_mock.return_value = VerificationResult(response_data)

        score_before = captcha_field.score
        captcha_field.validate(f.RECAPTCHA_TOKEN)
        score_after = captcha_field.score

        self.assertIsNone(score_before)
        self.assertEqual(score_after, 0.7)

    @patch("django_recaptcha.enterprise.fields.verify_enterprise_v1_token")
    def test_submitting_additional_info(self, verify_mock):
        """Additional info is also submitted after being provided."""
        captcha_field = ReCAPTCHAEnterpriseV1Field(
            project_id="<PROJECT-ID>",
            sitekey=f.SITEKEY,
            access_token="<ACCESS-TOKEN>",
        )
        http_request = MagicMock()
        http_request.build_absolute_uri.return_value = "http://example.com/"
        http_request.META = {
            "HTTP_USER_AGENT": "<CLIENT-USER-AGENT>",
            "REMOTE_ADDR": "1.2.3.4",
        }

        captcha_field.add_additional_info(http_request)
        captcha_field.validate(f.RECAPTCHA_TOKEN)

        http_request.build_absolute_uri.assert_called_once()
        verify_mock.assert_called_once_with(
            "<PROJECT-ID>",
            f.SITEKEY,
            "<ACCESS-TOKEN>",
            f.RECAPTCHA_TOKEN,
            None,
            "http://example.com/",
            "<CLIENT-USER-AGENT>",
            "1.2.3.4",
        )
