from typing import Any, Optional

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


class ReCAPTCHAEnterpriseNoWidget(Widget):
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

    def value_from_datadict(self, data: Any, files: Any, name: str) -> Any:
        return data.get("g-recaptcha-response", None)

    def value_omitted_from_data(self, data: Any, files: Any, name: str) -> bool:
        return "g-recaptcha-response" not in data


class ReCAPTCHAEnterpriseV1CheckboxWidget(Widget):
    """Widget for reCAPTCHA Enterprise V1 Checkbox."""

    template_name = "django_recaptcha/enterprise/widget_enterprise_v1_checkbox.html"

    def __init__(self, attrs: Optional[dict[str, Any]] = None):
        super().__init__(attrs)
        extend_class_attr(self.attrs, ["g-recaptcha"])

    def value_from_datadict(self, data: Any, files: Any, name: str) -> Any:
        return data.get("g-recaptcha-response", None)

    def value_omitted_from_data(self, data: Any, files: Any, name: str) -> bool:
        return "g-recaptcha-response" not in data

    def get_context(
        self, name: str, value: Any, attrs: Optional[dict[str, Any]]
    ) -> dict[str, Any]:
        context = super().get_context(name, value, attrs)
        context.update(
            {
                "script": {
                    "recaptcha_domain": use_setting(
                        "RECAPTCHA_ENTERPRISE_FRONTEND_DOMAIN"
                    ),
                }
            }
        )
        return context
