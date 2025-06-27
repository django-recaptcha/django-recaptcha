from django.test import TestCase
from django.utils.datastructures import MultiValueDict

from django_recaptcha.enterprise.widgets import ReCAPTCHAEnterpriseNoWidget


class ReCAPTCHAEnterpriseNoWidgetTest(TestCase):
    """Tests of the ReCAPTCHAEnterpriseNoWidget class."""

    def test_render(self):
        """Widget's rendering should be an empty string."""
        widget = ReCAPTCHAEnterpriseNoWidget()

        result = widget.render("field_name", "field_value")

        self.assertEqual(result, "")

    def test_value_from_datadict__value_provided(self):
        """Should return reCAPTCHA token if token is present in form data."""
        widget = ReCAPTCHAEnterpriseNoWidget()
        form_data = {"g-recaptcha-response": "<RECAPTCHA-TOKEN>"}
        files = MultiValueDict()
        name = "captcha"

        result = widget.value_from_datadict(form_data, files, name)

        self.assertEqual(result, "<RECAPTCHA-TOKEN>")

    def test_value_from_datadict__value_not_provided(self):
        """Should return None if token is not present in form data."""
        widget = ReCAPTCHAEnterpriseNoWidget()
        form_data = {}
        files = MultiValueDict()
        name = "captcha"

        result = widget.value_from_datadict(form_data, files, name)

        self.assertIsNone(result)

    def test_value_omitted_from_data__value_provided(self):
        """Should return False if token is present in form data."""
        widget = ReCAPTCHAEnterpriseNoWidget()
        form_data = {"g-recaptcha-response": "<RECAPTCHA-TOKEN>"}
        files = MultiValueDict()
        field_name = "captcha"

        result = widget.value_omitted_from_data(form_data, files, field_name)

        self.assertFalse(result)

    def test_value_omitted_from_data__value_not_provided(self):
        """Should return True if token is not present in form data."""
        widget = ReCAPTCHAEnterpriseNoWidget()
        form_data = {}
        files = MultiValueDict()
        field_name = "captcha"

        result = widget.value_omitted_from_data(form_data, files, field_name)

        self.assertTrue(result)
