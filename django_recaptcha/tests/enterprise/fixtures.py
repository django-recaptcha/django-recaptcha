RECAPTCHA_TOKEN = "<RECAPTCHA-TOKEN>"  # e.g. "03AF...EV2o"
SITEKEY = "<SITEKEY>"                  # e.g. "6Ldc...7GNA
ASSESSMENT_ID = "<ASSESSMENT_ID>"      # e.g. "projects/85...68/assessments/f8..00"


def create_request_data():
    return {
        "event": {
           "token": RECAPTCHA_TOKEN,
           "siteKey": SITEKEY,
        },
    }


def create_response_data(valid: bool = True):
    return {
        "name": ASSESSMENT_ID,
        "event": {
            "token": RECAPTCHA_TOKEN,
            "siteKey": SITEKEY,
            "userAgent": "",
            "userIpAddress": "",
            "expectedAction": "",
            "hashedAccountId": "",
            "express": False,
            "requestedUri": "",
            "wafTokenAssessment": False,
            "ja3": "",
            "ja4": "",
            "headers": [],
            "firewallPolicyEvaluation": False,
            "fraudPrevention": "FRAUD_PREVENTION_UNSPECIFIED"
        },
        "riskAnalysis": {
            "score": 0.4,
            "reasons": [],
            "extendedVerdictReasons": [],
            "challenge": "CHALLENGE_UNSPECIFIED",
            "verifiedBots": []
        },
        "tokenProperties": {
            "valid": valid,
            "invalidReason": "INVALID_REASON_UNSPECIFIED" if valid else "EXPIRED",
            "hostname": "localhost",
            "androidPackageName": "",
            "iosBundleId": "",
            "action": "LOGIN",
            "createTime": "2025-06-26T15:15:13.551Z"
        },
        "accountDefenderAssessment": {
            "labels": []
        }
    }
