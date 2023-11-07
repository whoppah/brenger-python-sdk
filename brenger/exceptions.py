class BrengerAPIException(Exception):
    """Base exception for all Brenger API related errors."""


class APIClientError(BrengerAPIException):
    """Exception raised when there's an error on the client side (e.g., bad request)."""


class APIServerError(BrengerAPIException):
    """Exception raised when the API server encounters an error (e.g., internal server error)."""
