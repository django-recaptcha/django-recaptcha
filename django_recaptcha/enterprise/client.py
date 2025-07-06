"""
Client used to communicate with the reCAPTCHA Enterprise API.

This module implements the following:

- making an API call to create an assessment
- making an API call to annotate an existing assessment (TODO)
- sending a request to the API

For more information: https://cloud.google.com/recaptcha/docs/reference/rest/v1/projects.assessments
"""

import json
from typing import Any, Optional, cast
from urllib.error import URLError
from urllib.request import ProxyHandler, Request, build_opener

from .conf import use_setting
from .exception import MissingAssessmentData, ReCAPTCHAEnterpriseAPICallFailed


class Assessment:
    """The data sent back by the reCAPTCHA Enterprise API after an assessment.

    :ivar dict[str, Any] data: response data
    """

    def __init__(self, response_data: dict[str, Any]) -> None:
        """
        :param response_data: data returned by API
        """
        self.data = response_data

    def is_token_valid(self) -> bool:
        """Check if the submitted reCAPTCHA token was valid or not.

        The token submitted by a user may be invalid for various reasons:
        being expired, being forged, etc. In addition, the action associated
        with the token might not match the expected action.

        :raises MissingAssessmentData: needed data is missing
        """
        try:
            is_valid: bool = self.data["tokenProperties"]["valid"]
            token_action: str = self.data["tokenProperties"]["action"]
            expected_action: str = self.data["event"]["expectedAction"]
            return is_valid and token_action == expected_action
        except KeyError as e:
            raise MissingAssessmentData(
                f"Object with key '{e.args[0]}' is missing from assessment data."
            )

    @property
    def score(self) -> float:
        """Returns score representing the assessed legitimacy of a user interaction.

        This score is a value between 0.0 and 1.0. A value being closer to one
        extreme indicates that the user interaction is more likely to be:

        - 0.0: fraudulent (high risk of fraud)
        - 1.0: legitimate (low-risk of fraud)

        :raises MissingAssessmentData: needed data is missing
        """
        try:
            score: float = self.data["riskAnalysis"]["score"]
            return score
        except KeyError as e:
            raise MissingAssessmentData(
                f"Object with key '{e.args[0]}' is missing from assessment data."
            )


def create_assessment(
    project_id: str,
    site_key: str,
    access_token: str,
    recaptcha_token: str,
    expected_action: Optional[str] = None,
    requested_uri: Optional[str] = None,
    user_agent: Optional[str] = None,
    user_ip_address: Optional[str] = None,
) -> Assessment:
    """Makes an API call to assess the risk associated with a user interaction.

    :param project_id: ID of Google Cloud project associated with site key
    :param site_key: public key used to integrate reCAPTCHA
    :param access_token: secret token used for authentication
    :param recaptcha_token: reCAPTCHA token submitted by user
    :param expected_action: action expected to be associated with reCAPTCHA token
    :param requested_uri: URI of resource requested by user
    :param user_agent: the user's user-agent string
    :param user_ip_address: the user's IP address
    :raises ReCAPTCHAEnterpriseAPICallFailed: sth went wrong during API call
    """
    url = f"https://recaptchaenterprise.googleapis.com/v1/projects/{project_id}/assessments"
    request_data = {
        "event": {
            "token": recaptcha_token,
            "siteKey": site_key,
        },
        "assessmentEnvironment": {
            "client": "pypi.org/project/django-recaptcha/",
            "version": "4.2.0",
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
    try:
        response_data = send_request(url, access_token, request_data)
    except ReCAPTCHAEnterpriseAPICallFailed as e:
        e.add_note("failed during call: projects.assessments.create")
        raise
    return Assessment(response_data)


def send_request(
    url: str,
    access_token: str,
    request_data: dict[str, Any],
) -> dict[str, Any]:
    """Send request data to Google's API endpoint and return response data.

    :param url: URL of API endpoint
    :param access_token: secret token used for authentication
    :param request_data: data sent with request
    :raises ReCAPTCHAEnterpriseAPICallFailed: sth went wrong during API call
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

    try:
        response = opener.open(request, timeout=timeout)
    except URLError as e:
        raise ReCAPTCHAEnterpriseAPICallFailed("API call failed.") from e

    response_body = response.read()
    response_data: dict[str, Any] = json.loads(response_body.decode("utf-8"))
    return response_data
