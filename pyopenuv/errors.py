"""Define package errors."""
from __future__ import annotations

from typing import Any


class OpenUvError(Exception):
    """Define a base error."""

    pass


class ApiUnavailableError(OpenUvError):
    """Define an error related to the OpenUV API being down."""

    pass


class InvalidApiKeyError(OpenUvError):
    """Define an error related to invalid API keys."""

    pass


class RateLimitExceededError(OpenUvError):
    """Define an error related to exceeding the daily rate limit."""

    pass


class RequestError(OpenUvError):
    """Define an error related to invalid requests."""

    pass


ERROR_MESSAGE_MAP = {
    "User with API Key not found": InvalidApiKeyError,
    "Daily API quota exceeded": RateLimitExceededError,
}


def raise_error(
    endpoint: str, payload: dict[str, Any], raising_err: Exception | None
) -> None:
    """Raise the appropriate error based on the response data.

    Args:
        endpoint: The endpoint that was queried.
        payload: An API response payload.
        raising_err: The exception that caused the overall issue.

    Raises:
        exc: Raised upon an HTTP error.
    """
    if (error_msg := payload.get("error")) is None:
        return

    try:
        exc = next(exc for idx, exc in ERROR_MESSAGE_MAP.items() if idx in error_msg)
    except StopIteration:
        exc = RequestError

    exc.__cause__ = raising_err
    raise exc(f"Error while querying {endpoint}: {error_msg}")
