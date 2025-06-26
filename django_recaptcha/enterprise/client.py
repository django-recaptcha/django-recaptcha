import json
from typing import Any
from urllib.request import ProxyHandler, Request, build_opener

from django.conf import settings


class VerificationResult:
    """The results sent back by Google after token verification.

    :ivar Any data: direct reference to data returned by Google; use with care
    """

    def __init__(self, response_data: dict[str,Any]) -> None:
        """
        :param response_data: data from response with results
        """
        self.data = response_data

    def is_okay(self) -> bool:
        """Check if token passes verification or not.
        """
        return self.data["tokenProperties"]["valid"]


def verify_enterprise_v1_token(
        project_id: str,
        sitekey: str,
        access_token: str,
        recaptcha_token: str,
    ) -> VerificationResult:
    """Verifies a reCAPTCHA Enterprise v1 token submitted by user.

    :param project_id: ID of Google cloud project associated with sitekey
    :param sitekey: your unique reCAPTCHA key
    :param access_token: access token of used to authenticate with API
    :param recaptcha_token: reCAPTCHA token submitted by user
    """
    url = f"https://recaptchaenterprise.googleapis.com/v1/projects/{project_id}/assessments"
    request_data = {
        "event": {
            "token": recaptcha_token,
            "siteKey": sitekey,
        },
    }
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
    proxies = getattr(settings, "RECAPTCHA_ENTERPRISE_PROXY", {})
    timeout = getattr(settings, "RECAPTCHA_ENTERPRISE_TIMEOUT", 10.0)

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

    return response_data
