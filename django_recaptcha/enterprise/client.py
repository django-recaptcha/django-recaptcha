from typing import Any


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
    :param access_token: access token of service account used to access API
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
        body: dict[str,Any],
    ) -> dict[str,Any]:
        pass
