"""Define package errors."""


class OpenUvError(Exception):
    """Define a base error."""

    pass


class InvalidApiKeyError(OpenUvError):
    """Define an error related to invalid API keys."""

    pass


class RequestError(OpenUvError):
    """Define an error related to invalid requests."""

    pass
