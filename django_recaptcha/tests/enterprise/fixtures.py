from typing import Any, Optional

RECAPTCHA_TOKEN = "<RECAPTCHA-TOKEN>"  # e.g. "03AF...EV2o"
SITEKEY = "<SITEKEY>"  # e.g. "6Ldc...7GNA
ASSESSMENT_ID = "<ASSESSMENT_ID>"  # e.g. "projects/85...68/assessments/f8..00"


def create_request_data(
    action: Optional[str] = None,
    requested_uri: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> dict[str, Any]:
    data = {
        "event": {
            "token": RECAPTCHA_TOKEN,
            "siteKey": SITEKEY,
        },
    }
    if action:
        data["event"]["expectedAction"] = action
    if requested_uri:
        data["event"]["requestedUri"] = requested_uri
    if user_agent:
        data["event"]["userAgent"] = user_agent
    return data


def create_response_data(
    valid: bool = True,
    client_action: str = "",
    expected_action: str = "",
    score: float = 0.4,
    requested_uri: str = "",
    user_agent: str = "",
) -> dict[str, Any]:
    return {
        "name": ASSESSMENT_ID,
        "event": {
            "token": RECAPTCHA_TOKEN,
            "siteKey": SITEKEY,
            "userAgent": user_agent,
            "userIpAddress": "",
            "expectedAction": expected_action,
            "hashedAccountId": "",
            "express": False,
            "requestedUri": requested_uri,
            "wafTokenAssessment": False,
            "ja3": "",
            "ja4": "",
            "headers": [],
            "firewallPolicyEvaluation": False,
            "fraudPrevention": "FRAUD_PREVENTION_UNSPECIFIED",
        },
        "riskAnalysis": {
            "score": score if valid else 0,
            "reasons": [],
            "extendedVerdictReasons": [],
            "challenge": "CHALLENGE_UNSPECIFIED",
            "verifiedBots": [],
        },
        "tokenProperties": {
            "valid": valid,
            "invalidReason": "INVALID_REASON_UNSPECIFIED" if valid else "EXPIRED",
            "hostname": "localhost",
            "androidPackageName": "",
            "iosBundleId": "",
            "action": client_action if client_action else "",
            "createTime": "2025-06-26T15:15:13.551Z",
        },
        "accountDefenderAssessment": {"labels": []},
    }
