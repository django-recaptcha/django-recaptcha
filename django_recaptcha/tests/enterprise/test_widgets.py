from django.test import TestCase
from django.utils.datastructures import MultiValueDict

from django_recaptcha.enterprise.widgets import (
    ReCAPTCHAEnterpriseNoWidget,
    ReCAPTCHAEnterpriseV1CheckboxWidget,
)


class ReCAPTCHAEnterpriseNoWidgetTest(TestCase):
    """Tests of the ReCAPTCHAEnterpriseNoWidget class."""

    def test_render(self):
        """Widget's rendering should be an empty string."""
        widget = ReCAPTCHAEnterpriseNoWidget()

        result = widget.render("field_name", "field_value")

        self.assertHTMLEqual(result, "")

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


class ReCAPTCHAEnterpriseV1CheckboxWidgetTests(TestCase):
    """Tests of the ReCAPTCHAEnterpriseV1CheckboxWidget class."""

    def test_render(self):
        """Widget's rendering should be as expected."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget(attrs={"class": "g-recaptcha"})

        result = widget.render("field_name", "field_value")

        self.assertHTMLEqual(
            result,
            """
            <script src="https://www.google.com/recaptcha/enterprise.js" async defer></script>
            <div class="g-recaptcha" data-sitekey="SITEKEY"></div>
            """)

    def test_value_from_datadict__value_provided(self):
        """Should return reCAPTCHA token if token is present in form data."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget(attrs={"class": "g-recaptcha"})
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
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget(attrs={"class": "g-recaptcha"})
        form_data = {"g-recaptcha-response": "<RECAPTCHA-TOKEN>"}
        files = MultiValueDict()
        field_name = "captcha"

        result = widget.value_omitted_from_data(form_data, files, field_name)

        self.assertFalse(result)

    def test_value_omitted_from_data__value_not_provided(self):
        """Should return True if token is not present in form data."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget(attrs={"class": "g-recaptcha"})
        form_data = {}
        files = MultiValueDict()
        field_name = "captcha"

        result = widget.value_omitted_from_data(form_data, files, field_name)

        self.assertTrue(result)
