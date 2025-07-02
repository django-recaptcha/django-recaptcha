from django.test import TestCase, override_settings
from django.utils.datastructures import MultiValueDict

from django_recaptcha.enterprise.widgets import (
    ReCAPTCHAEnterpriseNoWidget,
    ReCAPTCHAEnterpriseV1CheckboxWidget,
    extend_class_attr,
)


class ExtendClassAttributeTests(TestCase):
    """Tests the ``extend_class_attribute()`` function.

    Test design is based on the following parameters:

    - how many extra classes?
        * no extra classes
        * 1 extra class
        * 2 extra classes
    - existing attrs variable
        * empty
        * class attribute with 0 classes
        * class attribute with 1 classes
        * class attribute with 2 classes
    - how many extra classes are already present?
        * 0
        * 1
        * 2

    Ignore the combinations that aren't possible.
    e.g. no extra classes + 2 extra classes already present

    The same class may be present multiple times, so consider this too.
    Then, also take note of the order in which classes appear:

    - there's no significant difference between classA, classB, ...
    - there's a significant difference between class1, class2, ...
    """

    def test__no_extra_classes(self):
        extra_classes = []
        matrix = [
            ({}, {}),  # no need to add an empty class attribute
            (
                {"class": ""},
                {"class": ""},
            ),  # keep empty class attribute if already present
            ({"class": "classA"}, {"class": "classA"}),
            ({"class": "classA classB"}, {"class": "classA classB"}),
        ]

        for attrs, expected in matrix:
            extend_class_attr(attrs, extra_classes)
            self.assertEqual(attrs, expected)

    def test__one_extra_class(self):
        extra_classes = ["class1"]
        matrix = [
            ({}, {"class": "class1"}),
            ({"class": ""}, {"class": "class1"}),
            ({"class": "classA"}, {"class": "classA class1"}),
            ({"class": "class1"}, {"class": "class1"}),
            ({"class": "classA classB"}, {"class": "classA classB class1"}),
            ({"class": "classA class1"}, {"class": "classA class1"}),
            ({"class": "class1 classA"}, {"class": "class1 classA"}),
            ({"class": "class1 class1"}, {"class": "class1 class1"}),
        ]

        for attrs, expected in matrix:
            extend_class_attr(attrs, extra_classes)
            self.assertEqual(attrs, expected)

    def test__two_extra_classes(self):
        extra_classes = ["class1", "class2"]
        matrix = [
            ({}, {"class": "class1 class2"}),
            ({"class": ""}, {"class": "class1 class2"}),
            ({"class": "classA"}, {"class": "classA class1 class2"}),
            ({"class": "class1"}, {"class": "class1 class2"}),
            ({"class": "class2"}, {"class": "class2 class1"}),
            ({"class": "classA classB"}, {"class": "classA classB class1 class2"}),
            ({"class": "classA class1"}, {"class": "classA class1 class2"}),
            ({"class": "classA class2"}, {"class": "classA class2 class1"}),
            ({"class": "class1 classA"}, {"class": "class1 classA class2"}),
            ({"class": "class1 class1"}, {"class": "class1 class1 class2"}),
            ({"class": "class1 class2"}, {"class": "class1 class2"}),
            ({"class": "class2 classA"}, {"class": "class2 classA class1"}),
            ({"class": "class2 class1"}, {"class": "class2 class1"}),
            ({"class": "class2 class2"}, {"class": "class2 class2 class1"}),
        ]

        for attrs, expected in matrix:
            extend_class_attr(attrs, extra_classes)
            self.assertEqual(attrs, expected)


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
    """Tests the ReCAPTCHAEnterpriseV1CheckboxWidget class."""

    def test_render__default(self):
        """Should render the default widget if not altered in any way."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget()
        widget.attrs["data-sitekey"] = "SITEKEY"  # done by field

        result = widget.render("field_name", "field_value")

        self.assertHTMLEqual(
            result,
            """
            <script src="https://www.google.com/recaptcha/enterprise.js" async defer></script>
            <div class="g-recaptcha" data-sitekey="SITEKEY"></div>
            """,
        )

    def test_render__without_script_tag(self):
        """Should render the widget without script tag."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget(api_script_include=False)
        widget.attrs["data-sitekey"] = "SITEKEY"  # done by field

        result = widget.render("field_name", "field_value")

        self.assertHTMLEqual(
            result,
            """
            <div class="g-recaptcha" data-sitekey="SITEKEY"></div>
            """,
        )

    def test_render__different_domain(self):
        """Should render the widget with a different domain for its API script."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget(
            api_script_domain="www.recaptcha.net"
        )
        widget.attrs["data-sitekey"] = "SITEKEY"  # done by field

        result = widget.render("field_name", "field_value")

        self.assertHTMLEqual(
            result,
            """
            <script src="https://www.recaptcha.net/recaptcha/enterprise.js" async defer></script>
            <div class="g-recaptcha" data-sitekey="SITEKEY"></div>
            """,
        )

    def test_value_from_datadict__value_provided(self):
        """Should return reCAPTCHA token if token is present in form data."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget()
        form_data = {"g-recaptcha-response": "<RECAPTCHA-TOKEN>"}
        files = MultiValueDict()
        name = "captcha"

        result = widget.value_from_datadict(form_data, files, name)

        self.assertEqual(result, "<RECAPTCHA-TOKEN>")

    def test_value_from_datadict__value_not_provided(self):
        """Should return None if reCAPTCHA token is not present in form data."""
        widget = ReCAPTCHAEnterpriseNoWidget()
        form_data = {}
        files = MultiValueDict()
        name = "captcha"

        result = widget.value_from_datadict(form_data, files, name)

        self.assertIsNone(result)

    def test_value_omitted_from_data__value_provided(self):
        """Should return False if token is present in form data."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget()
        form_data = {"g-recaptcha-response": "<RECAPTCHA-TOKEN>"}
        files = MultiValueDict()
        field_name = "captcha"

        result = widget.value_omitted_from_data(form_data, files, field_name)

        self.assertFalse(result)

    def test_value_omitted_from_data__value_not_provided(self):
        """Should return True if token is not present in form data."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget()
        form_data = {}
        files = MultiValueDict()
        field_name = "captcha"

        result = widget.value_omitted_from_data(form_data, files, field_name)

        self.assertTrue(result)

    def test_get_context__default_values(self):
        """Should add default values to context if not altered in any way."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget()
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertTrue(context["api_script"]["include"])
        self.assertEqual(context["api_script"]["domain"], "www.google.com")

    @override_settings(RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_INCLUDE=False)
    def test_get_context__exclude_api_script_via_django_setting(self):
        """Should set context variable to exclude script tag via a Django setting."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget()
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertFalse(context["api_script"]["include"])

    def test_get_context__exclude_api_script_via_parameter(self):
        """Should set context variable to exclude script tag via a parameter."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget(api_script_include=False)
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertFalse(context["api_script"]["include"])

    @override_settings(
        RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_DOMAIN="www.recaptcha.net"
    )
    def test_get_context__set_script_frontend_domain_via_django_setting(self):
        """Should change context variable of API script's domain via a Django setting."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget()
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertEqual(context["api_script"]["domain"], "www.recaptcha.net")

    def test_get_context__set_script_domain_via_parameter(self):
        """Should change context variable of API script's domain via a parameter."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget(
            api_script_domain="www.recaptcha.net"
        )
        name = "<NAME>"
        value = "<VALUE>"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertEqual(context["api_script"]["domain"], "www.recaptcha.net")
