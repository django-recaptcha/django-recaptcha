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
