import json
from typing import Any, cast, Optional
from urllib.request import ProxyHandler, Request, build_opener

from .conf import use_setting



class VerificationResult:
    """The results sent back by Google after token verification.

    :ivar Any data: direct reference to data returned by Google
    """

    def __init__(self, response_data: dict[str,Any]) -> None:
        """
        :param response_data: data returned by Google
        """
        self.data = response_data

    def is_okay(self) -> bool:
        """Check if token passes verification or not."""
        if not self.data["tokenProperties"]["valid"]:
            return False
        if self.data["event"]["expectedAction"] != self.data["tokenProperties"]["action"]:
            return False
        return True


def verify_enterprise_v1_token(
        project_id: str,
        sitekey: str,
        access_token: str,
        recaptcha_token: str,
        expected_action: Optional[str] = None,
    ) -> VerificationResult:
    """Verifies a reCAPTCHA Enterprise v1 token submitted by user.

    :param project_id: ID of Google cloud project associated with sitekey
    :param sitekey: your unique reCAPTCHA key
    :param access_token: access token of used to authenticate with API
    :param recaptcha_token: reCAPTCHA token submitted by user
    :param expected_action: action corresponding to the token
    """
    url = f"https://recaptchaenterprise.googleapis.com/v1/projects/{project_id}/assessments"
    request_data = {
        "event": {
            "token": recaptcha_token,
            "siteKey": sitekey,
        },
    }
    if expected_action is not None:
        request_data["expectedAction"] = expected_action
    response_data = send_request(url, access_token, request_data)
    return VerificationResult(response_data)


def send_request(
        url: str,
        access_token: str,
        request_data: dict[str,Any],
    ) -> dict[str,Any]:
    """Send request data to Google's API endpoint and return response data.

    :param url: URL of API endpoint
    :param access_token: access token of used to authenticate with API
    :param request_data: raw data sent with request
    """
    proxies = use_setting("RECAPTCHA_ENTERPRISE_PROXY")
    timeout = use_setting("RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT")

    request_body = json.dumps(request_data).encode("utf-8")
    additional_headers = {
        "X-goog-api-key": access_token,
        "Content-Type": "application/json; charset=utf-8",
    }

    request = Request(url=url, data=request_body, headers=additional_headers, method="POST")

    opener_args = [ProxyHandler(proxies)] if proxies else []
    opener = build_opener(*opener_args)

    response = opener.open(request, timeout=timeout)
    response_body = response.read()
    response_data = json.loads(response_body.decode("utf-8"))

    response_data = cast(dict[str,Any], response_data)
    return response_data
