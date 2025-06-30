from typing import Any, Optional

from django.conf import settings

_DEFAULT_SETTINGS: dict[str, Any] = {
    # ID of Google cloud project associated with sitekey
    # e.g. "my-project-123456"
    "RECAPTCHA_ENTERPRISE_PROJECT_ID": None,
    # public key used to integrate reCAPTCHA
    # e.g. "6Lcm3XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX5mfX"
    "RECAPTCHA_ENTERPRISE_SITEKEY": None,
    # API key used for authentication
    # e.g. "ABcdEfG12jKlMNo3pqRsTUvWXYzA4BCDEf5hiJk"
    "RECAPTCHA_ENTERPRISE_ACCESS_TOKEN": None,
    # minimum score needed to pass validation (value between 0.0 and 1.0)
    # e.g. 0.1
    "RECAPTCHA_ENTERPRISE_REQUIRED_SCORE": None,
    # Configuration for usage of proxies.
    # e.g. {"https": "https://127.0.0.1:56789"}
    "RECAPTCHA_ENTERPRISE_PROXY": {},
    # Amount of seconds to wait until attempt to verify token times out.
    # e.g. 5.0
    "RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT": 10.0,
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
