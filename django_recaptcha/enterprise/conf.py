"""Settings used by this app.

This module documents all of the settings used to configure this app, and
their default values. Users will need to provide values for some settings in
order for this app to work properly, while other settings have sane defaults.

It also includes a function that is used internally to prioritize between an
argument or Django setting provided by the user, or its default value.
"""

from typing import Any, Optional

from django.conf import settings

_DEFAULT_SETTINGS: dict[str, Any] = {
    # ID of Google Cloud project associated with site key.
    # e.g. "my-project-123456"
    "RECAPTCHA_ENTERPRISE_PROJECT_ID": None,
    # Public key used to integrate reCAPTCHA.
    # e.g. "6Lcm3XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX5mfX"
    "RECAPTCHA_ENTERPRISE_SITEKEY": None,
    # Secret token used for authentication.
    # e.g. "ABcdEfG12jKlMNo3pqRsTUvWXYzA4BCDEf5hiJk"
    "RECAPTCHA_ENTERPRISE_ACCESS_TOKEN": None,
    # Configuration of proxies used to communicate with reCAPTCHA Enterprise API.
    # e.g. {"https": "https://127.0.0.1:56789"}
    "RECAPTCHA_ENTERPRISE_PROXY": {},
    # Amount of seconds until an API call times out.
    # e.g. 5.0
    "RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT": 10.0,
    # Include reCAPTCHA Enterprise's API script with each widget?
    # e.g. False
    "RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_INCLUDE": True,
    # If API script is included with widget: domain of its URL.
    # e.g. "www.recaptcha.net"
    "RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_DOMAIN": "www.google.com",
    # If API script is included with widget: query parameters of its URL.
    # e.g. {"render": "explicit", "onload": "renderAllWidgets", "hl": "nl"}
    "RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_PARAMETERS": {},
    # If API script is included with widget: attributes of its script tag.
    # e.g. {"async": True, "type": "module"}
    "RECAPTCHA_ENTERPRISE_WIDGET_API_SCRIPT_ATTRIBUTES": {"async": True, "defer": True},
}


def use_setting(name: str, value: Optional[Any] = None) -> Any:
    """Returns the value with the highest priority for this setting.

    The order of priority is as follows:

        1. value passed along as an argument
        2. value set by Django settings file
        3. default value set by this file

    :param name: name of setting
    :param value: used instead of Django setting or default value if provided
    """
    assert name in _DEFAULT_SETTINGS  # prevents typos and such
    if value is not None:
        return value
    default_value = _DEFAULT_SETTINGS.get(name)
    return getattr(settings, name, default_value)
