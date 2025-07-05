from typing import Any, Optional
from urllib.parse import urlencode

from django.forms.widgets import Widget

from .conf import use_setting


def extend_class_attr(attrs: dict[str, Any], extra_classes: list[str]) -> None:
    """Adds classes to widget's class attribute that aren't present yet."""
    class_attr_value: str = attrs.get("class", "")
    class_list = class_attr_value.split()
    for class_name in extra_classes:
        if class_name not in class_list:
            class_list.append(class_name)
    if class_list:
        attrs["class"] = " ".join(class_list)


class ReCAPTCHAEnterpriseV1Widget(Widget):
    """Common base class of reCAPTCHA Enterprise widgets."""

    def __init__(
        self,
        attrs: Optional[dict[str, Any]] = None,
        *,
        api_script_include: Optional[bool] = None,
        api_script_domain: Optional[str] = None,
        api_script_parameters: Optional[dict[str, Any]] = None,
        api_script_attributes: Optional[dict[str, Any]] = None,
    ):
        """
        :param api_script_include: include reCAPTCHA API script?
        :param api_script_domain: domain of API script's URL
        :param api_script_parameters: parameters of API script URL's query string
        :param api_script_attributes: attributes of API script's tag
        """
        super().__init__(attrs)
        self._api_script_include = use_setting(
            "RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_INCLUDE", api_script_include
        )
        self._api_script_domain = use_setting(
            "RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_DOMAIN", api_script_domain
        )
        self._api_script_parameters = use_setting(
            "RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_PARAMETERS", api_script_parameters
        )
        self._api_script_attributes = use_setting(
            "RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_ATTRIBUTES", api_script_attributes
        )
        self._action: Optional[str] = None  # can be set by field
        self._sitekey: Optional[str] = None  # must be set by field afterwards!

    def set_action(self, action: str) -> None:
        self._action = action

    def set_sitekey(self, sitekey: str) -> None:
        self._sitekey = sitekey

    def build_attrs(
        self, base_attrs: dict[str, Any], extra_attrs: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        attrs = super().build_attrs(base_attrs, extra_attrs)
        assert self._sitekey is not None  # should've been set by Field
        attrs["data-sitekey"] = self._sitekey
        if self._action:
            attrs["data-action"] = self._action or ""
        return attrs

    def get_context(
        self, name: str, value: Any, attrs: Optional[dict[str, Any]]
    ) -> dict[str, Any]:
        context = super().get_context(name, value, attrs)
        assert self._sitekey is not None  # should've been set by Field
        context.update(
            {
                "action": self._action,
                "sitekey": self._sitekey,
                "api_script": {
                    "include": self._api_script_include,
                    "domain": self._api_script_domain,
                    "attrs": self._api_script_attributes,
                },
            }
        )
        if self._api_script_parameters is not None:
            context["api_script"]["qs"] = urlencode(self._api_script_parameters)
        return context

    def value_from_datadict(self, data: Any, files: Any, name: str) -> Any:
        return data.get("g-recaptcha-response", None)

    def value_omitted_from_data(self, data: Any, files: Any, name: str) -> bool:
        return "g-recaptcha-response" not in data


class ReCAPTCHAEnterpriseNoHTMLRenderWidget(ReCAPTCHAEnterpriseV1Widget):
    """Used with reCAPTCHA fields for which no HTML is rendered.

    Using this widget is not recommended, unless you want to heavily customize
    the client-side integration of reCAPTCHA:

    - you'll have to load the reCAPTCHA API script yourself

    - if you rely on reCAPTCHA automatically rendering its elements once it
      finishes loading, do not forget to add ``g-recaptcha`` to the class
      attribute of every container and/or protected buttons; otherwise, call
      ``grecaptcha.render()`` once for each

    - you'll also need to make your sitekey and other attributes accessible in
      some other way, e.g.:
        - hardcode it in the form's HTML (not flexible)
        - inject it when rendering the view
        - ...

    You should not have to do anything different from other widgets on the
    server side. This widget can handle extracting the reCAPTCHA token
    submitted by the user from the form data.
    """

    template_name = "django_recaptcha/enterprise/no_widget.html"


class ReCAPTCHAEnterpriseV1CheckboxWidget(ReCAPTCHAEnterpriseV1Widget):
    """Widget for challenge-based reCAPTCHA Enterprise v1."""

    template_name = "django_recaptcha/enterprise/widget_enterprise_v1_checkbox.html"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        extend_class_attr(self.attrs, ["g-recaptcha"])


class ReCAPTCHAEnterpriseV1HiddenWidget(ReCAPTCHAEnterpriseV1Widget):
    """Widget for score-based reCAPTCHA Enterprise v1."""

    template_name = "django_recaptcha/enterprise/widget_enterprise_v1_hidden.html"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        extend_class_attr(self.attrs, ["django-recaptcha-widget-enterprise"])

    def build_attrs(
        self, base_attrs: dict[str, Any], extra_attrs: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["data-size"] = attrs.get("data-size", "invisible")
        return attrs

    def get_context(
        self, name: str, value: Any, attrs: Optional[dict[str, Any]]
    ) -> dict[str, Any]:
        context = super().get_context(name, value, attrs)
        assert self._sitekey is not None  # should've been set by Field

        aps = {}
        aps.update(self._api_script_parameters)
        aps["render"] = aps.get("render", self._sitekey)
        context["api_script"]["qs"] = urlencode(aps)

        return context
