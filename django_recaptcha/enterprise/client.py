import json
from typing import Any, Optional, cast
from urllib.request import ProxyHandler, Request, build_opener

from .conf import use_setting


class VerificationResult:
    """The results sent back by Google after token verification.

    :ivar dict[str, Any] data: direct reference to data returned by Google
    """

    def __init__(self, response_data: dict[str, Any]) -> None:
        """
        :param response_data: data returned in the response
        """
        self.data = response_data

    def is_okay(self, required_score: float) -> bool:
        """Check if token passes verification or not."""
        if not self.data["tokenProperties"]["valid"]:
            return False
        if (
            self.data["event"]["expectedAction"]
            != self.data["tokenProperties"]["action"]
        ):
            return False
        if float(self.data["riskAnalysis"]["score"]) < required_score:
            return False
        return True

    @property
    def score(self) -> float:
        """Returns score returned after token verification."""
        return cast(float, self.data["riskAnalysis"]["score"])


def verify_enterprise_v1_token(
    project_id: str,
    sitekey: str,
    access_token: str,
    recaptcha_token: str,
    expected_action: Optional[str] = None,
    requested_uri: Optional[str] = None,
    user_agent: Optional[str] = None,
    user_ip_address: Optional[str] = None,
) -> VerificationResult:
    """Verifies a reCAPTCHA Enterprise v1 token submitted by user.

    :param project_id: ID of Google cloud project associated with sitekey
    :param sitekey: public key used to integrate reCAPTCHA
    :param access_token: token used for authentication
    :param recaptcha_token: reCAPTCHA token submitted by user
    :param expected_action: action associated with reCAPTCHA token
    :param requested_uri: URI of resource accessed by user
    :param user_agent: the client's user-agent string
    :param user_ip_address: the user's IP address
    """
    url = f"https://recaptchaenterprise.googleapis.com/v1/projects/{project_id}/assessments"
    request_data = {
        "event": {
            "token": recaptcha_token,
            "siteKey": sitekey,
        },
    }
    if expected_action is not None:
        request_data["event"]["expectedAction"] = expected_action
    if requested_uri is not None:
        request_data["event"]["requestedUri"] = requested_uri
    if user_agent is not None:
        request_data["event"]["userAgent"] = user_agent
    if user_ip_address is not None:
        request_data["event"]["userIpAddress"] = user_ip_address
    response_data = send_request(url, access_token, request_data)
    return VerificationResult(response_data)


def send_request(
    url: str,
    access_token: str,
    request_data: dict[str, Any],
) -> dict[str, Any]:
    """Send request data to Google's API endpoint and return response data.

    :param url: URL of API endpoint
    :param access_token: token used for authentication
    :param request_data: data sent with request
    """
    proxies = use_setting("RECAPTCHA_ENTERPRISE_PROXY")
    timeout = use_setting("RECAPTCHA_ENTERPRISE_VERIFY_TIMEOUT")

    request_body = json.dumps(request_data).encode("utf-8")
    additional_headers = {
        "X-goog-api-key": access_token,
        "Content-Type": "application/json; charset=utf-8",
    }

    request = Request(
        url=url, data=request_body, headers=additional_headers, method="POST"
    )

    opener_args = [ProxyHandler(proxies)] if proxies else []
    opener = build_opener(*opener_args)

    response = opener.open(request, timeout=timeout)
    response_body = response.read()
    response_data = json.loads(response_body.decode("utf-8"))

    response_data = cast(dict[str, Any], response_data)
    return response_data
