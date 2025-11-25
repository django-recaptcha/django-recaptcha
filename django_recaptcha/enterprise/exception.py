"""Exceptions raised by this app."""


class MissingAssessmentData(Exception):
    """Needed data is missing from assessment data."""


class ReCAPTCHAEnterpriseAPICallFailed(Exception):
    """API call failed."""
