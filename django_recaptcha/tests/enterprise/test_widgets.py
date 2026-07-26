from django.test import TestCase, override_settings
from django.utils.datastructures import MultiValueDict

from django_recaptcha.enterprise.widgets import (
    ReCAPTCHAEnterpriseNoHTMLWidget,
    ReCAPTCHAEnterpriseV1CheckboxWidget,
    ReCAPTCHAEnterpriseV1HiddenWidget,
    extend_class_attr,
)


class ExtendClassAttributeTests(TestCase):
    """Tests the ``extend_class_attr()`` function.

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
            ("", ""),
            ("classA", "classA"),
            ("classA classB", "classA classB"),
        ]

        for original, expected in matrix:
            result = extend_class_attr(original, extra_classes)
            self.assertEqual(result, expected)

    def test__one_extra_class(self):
        extra_classes = ["class1"]
        matrix = [
            ("", "class1"),
            ("classA", "classA class1"),
            ("class1", "class1"),
            ("classA classB", "classA classB class1"),
            ("classA class1", "classA class1"),
            ("class1 classA", "class1 classA"),
            ("class1 class1", "class1 class1"),
        ]

        for original, expected in matrix:
            result = extend_class_attr(original, extra_classes)
            self.assertEqual(result, expected)

    def test__two_extra_classes(self):
        extra_classes = ["class1", "class2"]
        matrix = [
            ("", "class1 class2"),
            ("classA", "classA class1 class2"),
            ("class1", "class1 class2"),
            ("class2", "class2 class1"),
            ("classA classB", "classA classB class1 class2"),
            ("classA class1", "classA class1 class2"),
            ("classA class2", "classA class2 class1"),
            ("class1 classA", "class1 classA class2"),
            ("class1 class1", "class1 class1 class2"),
            ("class1 class2", "class1 class2"),
            ("class2 classA", "class2 classA class1"),
            ("class2 class1", "class2 class1"),
            ("class2 class2", "class2 class2 class1"),
        ]

        for original, expected in matrix:
            result = extend_class_attr(original, extra_classes)
            self.assertEqual(result, expected)


class ReCAPTCHAEnterpriseNoWidgetTest(TestCase):
    """Tests of the ReCAPTCHAEnterpriseNoWidget class."""

    def test_render(self):
        """Widget's rendering should be an empty string."""
        widget = ReCAPTCHAEnterpriseNoHTMLWidget()
        widget.set_sitekey("SITEKEY")

        result = widget.render("field_name", "field_value")

        self.assertHTMLEqual(result, "")

    def test_value_from_datadict__value_provided(self):
        """Should return reCAPTCHA token if token is present in form data."""
        widget = ReCAPTCHAEnterpriseNoHTMLWidget()
        widget.set_sitekey("SITEKEY")
        form_data = {"g-recaptcha-response": "<RECAPTCHA-TOKEN>"}
        files = MultiValueDict()
        name = "captcha"

        result = widget.value_from_datadict(form_data, files, name)

        self.assertEqual(result, "<RECAPTCHA-TOKEN>")

    def test_value_from_datadict__value_not_provided(self):
        """Should return None if token is not present in form data."""
        widget = ReCAPTCHAEnterpriseNoHTMLWidget()
        widget.set_sitekey("SITEKEY")
        form_data = {}
        files = MultiValueDict()
        name = "captcha"

        result = widget.value_from_datadict(form_data, files, name)

        self.assertIsNone(result)

    def test_value_omitted_from_data__value_provided(self):
        """Should return False if token is present in form data."""
        widget = ReCAPTCHAEnterpriseNoHTMLWidget()
        widget.set_sitekey("SITEKEY")
        form_data = {"g-recaptcha-response": "<RECAPTCHA-TOKEN>"}
        files = MultiValueDict()
        field_name = "captcha"

        result = widget.value_omitted_from_data(form_data, files, field_name)

        self.assertFalse(result)

    def test_value_omitted_from_data__value_not_provided(self):
        """Should return True if token is not present in form data."""
        widget = ReCAPTCHAEnterpriseNoHTMLWidget()
        widget.set_sitekey("SITEKEY")
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
        widget.set_sitekey("SITEKEY")

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
        widget.set_sitekey("SITEKEY")

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
        widget.set_sitekey("SITEKEY")

        result = widget.render("field_name", "field_value")

        self.assertHTMLEqual(
            result,
            """
            <script src="https://www.recaptcha.net/recaptcha/enterprise.js" async defer></script>
            <div class="g-recaptcha" data-sitekey="SITEKEY"></div>
            """,
        )

    def test_render__with_query_string(self):
        """Should render the widget with a query string for its API script."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget(
            api_script_parameters={"onload": "loadAllWidgets", "hl": "nl"}
        )
        widget.set_sitekey("SITEKEY")

        result = widget.render("field_name", "field_value")

        self.assertHTMLEqual(
            result,
            """
            <script src="https://www.google.com/recaptcha/enterprise.js?onload=loadAllWidgets&hl=nl" async defer></script>
            <div class="g-recaptcha" data-sitekey="SITEKEY"></div>
            """,
        )

    def test_render__with_different_script_attributes(self):
        """Should render the widget with other attributes for its API script's tag."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget(
            api_script_attributes={"type": "module"}
        )
        widget.set_sitekey("SITEKEY")

        result = widget.render("field_name", "field_value")

        self.assertHTMLEqual(
            result,
            """
            <script src="https://www.google.com/recaptcha/enterprise.js" type="module"></script>
            <div class="g-recaptcha" data-sitekey="SITEKEY"></div>
            """,
        )

    def test_value_from_datadict__value_provided(self):
        """Should return reCAPTCHA token if token is present in form data."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget()
        widget.set_sitekey("SITEKEY")
        form_data = {"g-recaptcha-response": "<RECAPTCHA-TOKEN>"}
        files = MultiValueDict()
        name = "captcha"

        result = widget.value_from_datadict(form_data, files, name)

        self.assertEqual(result, "<RECAPTCHA-TOKEN>")

    def test_value_from_datadict__value_not_provided(self):
        """Should return None if reCAPTCHA token is not present in form data."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget()
        widget.set_sitekey("SITEKEY")
        form_data = {}
        files = MultiValueDict()
        name = "captcha"

        result = widget.value_from_datadict(form_data, files, name)

        self.assertIsNone(result)

    def test_value_omitted_from_data__value_provided(self):
        """Should return False if token is present in form data."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget()
        widget.set_sitekey("SITEKEY")
        form_data = {"g-recaptcha-response": "<RECAPTCHA-TOKEN>"}
        files = MultiValueDict()
        field_name = "captcha"

        result = widget.value_omitted_from_data(form_data, files, field_name)

        self.assertFalse(result)

    def test_value_omitted_from_data__value_not_provided(self):
        """Should return True if token is not present in form data."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget()
        widget.set_sitekey("SITEKEY")
        form_data = {}
        files = MultiValueDict()
        field_name = "captcha"

        result = widget.value_omitted_from_data(form_data, files, field_name)

        self.assertTrue(result)

    def test_get_context__default_values(self):
        """Should add default values to context if not altered in any way."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget()
        widget.set_sitekey("SITEKEY")
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
        widget.set_sitekey("SITEKEY")
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertFalse(context["api_script"]["include"])

    def test_get_context__exclude_api_script_via_parameter(self):
        """Should set context variable to exclude script tag via a parameter."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget(api_script_include=False)
        widget.set_sitekey("SITEKEY")
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
        widget.set_sitekey("SITEKEY")
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
        widget.set_sitekey("SITEKEY")
        name = "<NAME>"
        value = "<VALUE>"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertEqual(context["api_script"]["domain"], "www.recaptcha.net")

    @override_settings(
        RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_PARAMETERS={
            "render": "explicit",
            "hl": "en",
        }
    )
    def test_get_context__set_script_query_string_via_django_setting(self):
        """Should set query string of API script's URL via a django setting."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget()
        widget.set_sitekey("SITEKEY")
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertEqual(context["api_script"]["qs"], "render=explicit&hl=en")

    def test_get_context__set_script_query_string_via_parameter(self):
        """Should set query string of API script's URL via parameter."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget(
            api_script_parameters={"render": "explicit", "hl": "en"}
        )
        widget.set_sitekey("SITEKEY")
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertEqual(context["api_script"]["qs"], "render=explicit&hl=en")

    @override_settings(
        RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_ATTRIBUTES={"type": "module"}
    )
    def test_get_context__set_script_attributes_via_django_setting(self):
        """Should set attributes of API script's tag via Django setting."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget()
        widget.set_sitekey("SITEKEY")
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertEqual(context["api_script"]["attrs"], {"type": "module"})

    def test_get_context__set_script_attributes_via_parameter(self):
        """Should set attributes of API script's tag via parameter."""
        widget = ReCAPTCHAEnterpriseV1CheckboxWidget(
            api_script_attributes={"type": "module"}
        )
        widget.set_sitekey("SITEKEY")
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertEqual(context["api_script"]["attrs"], {"type": "module"})

    def test_add_classes(self):
        """Should correctly add extra classes."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget()
        widget.set_sitekey("SITEKEY")

        before = widget.attrs.get("class", "")
        widget.add_classes(["abc"])
        after = widget.attrs.get("class")

        self.assertEqual(before, "django-recaptcha-widget-enterprise")
        self.assertEqual(after, "django-recaptcha-widget-enterprise abc")


class ReCAPTCHAEnterpriseV1HiddenWidgetTests(TestCase):
    """Tests the ReCAPTCHAEnterpriseV1HiddenWidget class."""

    def test_render__default(self):
        """Should render the default widget if not altered in any way."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget()
        widget.set_sitekey("SITEKEY")

        result = widget.render("field_name", "field_value")

        self.assertHTMLEqual(
            result,
            """
            <script src="https://www.google.com/recaptcha/enterprise.js?render=SITEKEY" async defer></script>
            <script src="django_recaptcha/js/widget_enterprise.js" async defer></script>
            <div class="django-recaptcha-widget-enterprise" data-size="invisible" data-sitekey="SITEKEY"></div>
            """,
        )

    def test_render__without_script_tag(self):
        """Should render the widget without script tag."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget(api_script_include=False)
        widget.set_sitekey("SITEKEY")

        result = widget.render("field_name", "field_value")

        self.assertHTMLEqual(
            result,
            """
            <div class="django-recaptcha-widget-enterprise" data-size="invisible" data-sitekey="SITEKEY"></div>
            """,
        )

    def test_render__different_domain(self):
        """Should render the widget with a different domain for its API script."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget(
            api_script_domain="www.recaptcha.net"
        )
        widget.set_sitekey("SITEKEY")

        result = widget.render("field_name", "field_value")

        self.assertHTMLEqual(
            result,
            """
            <script src="https://www.recaptcha.net/recaptcha/enterprise.js?render=SITEKEY" async defer></script>
            <script src="django_recaptcha/js/widget_enterprise.js" async defer></script>
            <div class="django-recaptcha-widget-enterprise" data-size="invisible" data-sitekey="SITEKEY"></div>
            """,
        )

    def test_render__with_query_string(self):
        """Should render the widget with a query string for its API script."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget(
            api_script_parameters={"onload": "loadAllWidgets", "hl": "nl"}
        )
        widget.set_sitekey("SITEKEY")

        result = widget.render("field_name", "field_value")

        self.assertHTMLEqual(
            result,
            """
            <script src="https://www.google.com/recaptcha/enterprise.js?onload=loadAllWidgets&hl=nl&render=SITEKEY" async defer></script>
            <script src="django_recaptcha/js/widget_enterprise.js" async defer></script>
            <div class="django-recaptcha-widget-enterprise" data-size="invisible" data-sitekey="SITEKEY"></div>
            """,
        )

    def test_render__with_query_string__render_conflict(self):
        pass

    def test_render__with_different_script_attributes(self):
        """Should render the widget with other attributes for its API script's tag."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget(
            api_script_attributes={"type": "module"}
        )
        widget.set_sitekey("SITEKEY")

        result = widget.render("field_name", "field_value")

        self.assertHTMLEqual(
            result,
            """
            <script src="https://www.google.com/recaptcha/enterprise.js?render=SITEKEY" type="module"></script>
            <script src="django_recaptcha/js/widget_enterprise.js" async defer></script>
            <div class="django-recaptcha-widget-enterprise" data-size="invisible" data-sitekey="SITEKEY"></div>
            """,
        )

    def test_value_from_datadict__value_provided(self):
        """Should return reCAPTCHA token if token is present in form data."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget()
        widget.set_sitekey("SITEKEY")
        form_data = {"g-recaptcha-response": "<RECAPTCHA-TOKEN>"}
        files = MultiValueDict()
        name = "captcha"

        result = widget.value_from_datadict(form_data, files, name)

        self.assertEqual(result, "<RECAPTCHA-TOKEN>")

    def test_value_from_datadict__value_not_provided(self):
        """Should return None if reCAPTCHA token is not present in form data."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget()
        widget.set_sitekey("SITEKEY")
        form_data = {}
        files = MultiValueDict()
        name = "captcha"

        result = widget.value_from_datadict(form_data, files, name)

        self.assertIsNone(result)

    def test_value_omitted_from_data__value_provided(self):
        """Should return False if token is present in form data."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget()
        widget.set_sitekey("SITEKEY")
        form_data = {"g-recaptcha-response": "<RECAPTCHA-TOKEN>"}
        files = MultiValueDict()
        field_name = "captcha"

        result = widget.value_omitted_from_data(form_data, files, field_name)

        self.assertFalse(result)

    def test_value_omitted_from_data__value_not_provided(self):
        """Should return True if token is not present in form data."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget()
        widget.set_sitekey("SITEKEY")
        form_data = {}
        files = MultiValueDict()
        field_name = "captcha"

        result = widget.value_omitted_from_data(form_data, files, field_name)

        self.assertTrue(result)

    def test_get_context__default_values(self):
        """Should add default values to context if not altered in any way."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget()
        widget.set_sitekey("SITEKEY")
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertTrue(context["api_script"]["include"])
        self.assertEqual(context["api_script"]["domain"], "www.google.com")

    @override_settings(RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_INCLUDE=False)
    def test_get_context__exclude_api_script_via_django_setting(self):
        """Should set context variable to exclude script tag via a Django setting."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget()
        widget.set_sitekey("SITEKEY")
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertFalse(context["api_script"]["include"])

    def test_get_context__exclude_api_script_via_parameter(self):
        """Should set context variable to exclude script tag via a parameter."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget(api_script_include=False)
        widget.set_sitekey("SITEKEY")
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
        widget = ReCAPTCHAEnterpriseV1HiddenWidget()
        widget.set_sitekey("SITEKEY")
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertEqual(context["api_script"]["domain"], "www.recaptcha.net")

    def test_get_context__set_script_domain_via_parameter(self):
        """Should change context variable of API script's domain via a parameter."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget(
            api_script_domain="www.recaptcha.net"
        )
        widget.set_sitekey("SITEKEY")
        name = "<NAME>"
        value = "<VALUE>"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertEqual(context["api_script"]["domain"], "www.recaptcha.net")

    @override_settings(
        RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_PARAMETERS={
            "render": "explicit",
            "hl": "en",
        }
    )
    def test_get_context__set_script_query_string_via_django_setting(self):
        """Should set query string of API script's URL via a django setting."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget()
        widget.set_sitekey("SITEKEY")
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertEqual(context["api_script"]["qs"], "render=explicit&hl=en")

    def test_get_context__set_script_query_string_via_parameter(self):
        """Should set query string of API script's URL via parameter."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget(
            api_script_parameters={"render": "explicit", "hl": "en"}
        )
        widget.set_sitekey("SITEKEY")
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertEqual(context["api_script"]["qs"], "render=explicit&hl=en")

    @override_settings(
        RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_ATTRIBUTES={"type": "module"}
    )
    def test_get_context__set_script_attributes_via_django_setting(self):
        """Should set attributes of API script's tag via Django setting."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget()
        widget.set_sitekey("SITEKEY")
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertEqual(context["api_script"]["attrs"], {"type": "module"})

    def test_get_context__set_script_attributes_via_parameter(self):
        """Should set attributes of API script's tag via parameter."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget(
            api_script_attributes={"type": "module"}
        )
        widget.set_sitekey("SITEKEY")
        name = "field_name"
        value = "field_value"
        attrs = {}

        context = widget.get_context(name, value, attrs)

        self.assertEqual(context["api_script"]["attrs"], {"type": "module"})

    def test_add_classes(self):
        """Should correctly add extra classes."""
        widget = ReCAPTCHAEnterpriseV1HiddenWidget()
        widget.set_sitekey("SITEKEY")

        before = widget.attrs.get("class", "")
        widget.add_classes(["abc"])
        after = widget.attrs.get("class")

        self.assertEqual(before, "django-recaptcha-widget-enterprise")
        self.assertEqual(after, "django-recaptcha-widget-enterprise abc")
