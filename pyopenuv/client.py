"""Define a client to interact with openuv.io."""
from __future__ import annotations

import asyncio
import logging
import sys
from collections.abc import Awaitable, Callable
from typing import Any, cast

import backoff
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from .const import LOGGER
from .errors import InvalidApiKeyError, RequestError

API_URL_SCAFFOLD = "https://api.openuv.io/api/v1"

DEFAULT_PROTECTION_HIGH = 3.5
DEFAULT_PROTECTION_LOW = 3.5
DEFAULT_REQUEST_RETRIES = 10
DEFAULT_TIMEOUT = 30


class Client:
    """Define the client."""

    def __init__(
        self,
        api_key: str,
        latitude: float,
        longitude: float,
        *,
        altitude: float = 0.0,
        logger: logging.Logger | None = None,
        request_retries: int = DEFAULT_REQUEST_RETRIES,
        session: ClientSession | None = None,
    ) -> None:
        """Initialize.

        Args:
            api_key: An OpenUV API key.
            latitude: A latitude.
            longitude: A longitude.
            altitude: An altitude.
            logger: An optional logger.
            request_retries: The number of retries for a failed request.
            session: An optional aiohttp ClientSession.
        """
        self._api_key = api_key
        self._request_retries = request_retries
        self._session = session
        self.altitude = str(altitude)
        self.latitude = str(latitude)
        self.longitude = str(longitude)

        if logger:
            self._logger = logger
        else:
            self._logger = LOGGER

        self.async_request = self._wrap_request_method(self._request_retries)

    async def _async_request(
        self, method: str, endpoint: str, **kwargs: dict[str, str]
    ) -> dict[str, Any]:
        """Make an API request.

        Args:
            method: An HTTP method.
            endpoint: A relative API endpoint.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            An API response payload.
        """
        kwargs.setdefault("headers", {})
        kwargs["headers"]["x-access-token"] = self._api_key

        kwargs.setdefault("params", {})
        kwargs["params"]["lat"] = self.latitude
        kwargs["params"]["lng"] = self.longitude
        kwargs["params"]["alt"] = self.altitude

        if use_running_session := self._session and not self._session.closed:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        async with session.request(
            method, f"{API_URL_SCAFFOLD}/{endpoint}", **kwargs
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()

        if not use_running_session:
            await session.close()

        self._logger.debug("Received data for %s: %s", endpoint, data)

        return cast(dict[str, Any], data)

    def _handle_on_giveup(self, _: dict[str, Any]) -> None:
        """Determine what exception to raise upon giveup.

        Raises:
            InvalidApiKeyError: Raised upon an invalid OpenUV API key.
            RequestError: Raised upon an underlying HTTP error.
        """
        err_info = sys.exc_info()
        err = err_info[1].with_traceback(err_info[2])  # type: ignore[union-attr]

        if self._is_unauthorized_exception(err):
            raise InvalidApiKeyError("Invalid API key") from err
        raise RequestError(err) from err

    @staticmethod
    def _is_unauthorized_exception(err: BaseException) -> bool:
        """Return whether an exception represents an unauthorized error.

        Args:
            err: Any BaseException subclass.

        Returns:
            Whether the exception indicates an authorization error.
        """
        return isinstance(err, ClientError) and any(
            code in str(err) for code in ("401", "403")
        )

    def _wrap_request_method(
        self, request_retries: int
    ) -> Callable[..., Awaitable[dict[str, Any]]]:
        """Wrap the request method in backoff/retry logic.

        Args:
            request_retries: The number of retries to give a failed request.

        Returns:
            A version of the request callable that can do retries.
        """
        return cast(
            Callable[..., Awaitable[dict[str, Any]]],
            backoff.on_exception(
                backoff.expo,
                (asyncio.TimeoutError, ClientError),
                logger=self._logger,
                max_tries=request_retries,
                on_giveup=self._handle_on_giveup,  # type: ignore[arg-type]
            )(self._async_request),
        )

    def disable_request_retries(self) -> None:
        """Disable the request retry mechanism."""
        self.async_request = self._wrap_request_method(1)

    def enable_request_retries(self) -> None:
        """Enable the request retry mechanism."""
        self.async_request = self._wrap_request_method(self._request_retries)

    async def uv_forecast(self) -> dict[str, Any]:
        """Get forecasted UV data.

        Returns:
            An API response payload.
        """
        return await self.async_request("get", "forecast")

    async def uv_index(self) -> dict[str, Any]:
        """Get current UV data.

        Returns:
            An API response payload.
        """
        return await self.async_request("get", "uv")

    async def uv_protection_window(
        self, low: float = DEFAULT_PROTECTION_LOW, high: float = DEFAULT_PROTECTION_HIGH
    ) -> dict[str, Any]:
        """Get data on when a UV protection window is.

        Args:
            low: The low end of the UV index to monitor.
            high: The high end of the UV index to monitor.

        Returns:
            An API response payload.
        """
        return await self.async_request(
            "get", "protection", params={"from": str(low), "to": str(high)}
        )
