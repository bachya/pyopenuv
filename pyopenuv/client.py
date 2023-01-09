"""Define a client to interact with openuv.io."""
from __future__ import annotations

import asyncio
import logging
from typing import Any, cast

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from .const import LOGGER
from .errors import ApiUnavailableError, InvalidApiKeyError, RequestError

API_URL_SCAFFOLD = "https://api.openuv.io/api/v1"

DEFAULT_PROTECTION_HIGH = 3.5
DEFAULT_PROTECTION_LOW = 3.5
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
        session: ClientSession | None = None,
        check_status_before_request: bool = False,
    ) -> None:
        """Initialize.

        Args:
            api_key: An OpenUV API key.
            latitude: A latitude.
            longitude: A longitude.
            altitude: An altitude.
            logger: An optional logger.
            session: An optional aiohttp ClientSession.
            check_status_before_request: Whether the API status should be checked prior
                to every request.
        """
        self._api_key = api_key
        self._session = session
        self.altitude = str(altitude)
        self.check_status_before_request = check_status_before_request
        self.latitude = str(latitude)
        self.longitude = str(longitude)

        if logger:
            self._logger = logger
        else:
            self._logger = LOGGER

    async def _async_check_api_status_if_required(self) -> None:
        """Check the status of the API if configured to do so.

        Raises:
            ApiUnavailableError: Raised when the API is unavailable.
        """
        if not self.check_status_before_request or await self.api_status():
            return

        raise ApiUnavailableError("The OpenUV API is unavailable")

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

        Raises:
            InvalidApiKeyError: Raised on an invalid API key.
            RequestError: Raised on an HTTP error or request timeout.
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

        data: dict[str, Any] = {}
        url = f"{API_URL_SCAFFOLD}/{endpoint}"

        try:
            async with session.request(method, url, **kwargs) as resp:
                try:
                    data = await resp.json()
                    resp.raise_for_status()
                except ClientError as err:
                    if resp.status in (401, 403):
                        raise InvalidApiKeyError("Invalid API key") from err

                    error_msg = data.get("error", str(err))
                    raise RequestError(
                        f"Error while querying {url}: {error_msg}"
                    ) from err
        except asyncio.TimeoutError as err:
            raise RequestError(
                f"Error while querying {url}: Request timed out"
            ) from err
        finally:
            if not use_running_session:
                await session.close()

        self._logger.debug("Data received for %s: %s", endpoint, data)

        return data

    async def api_statistics(self) -> dict[str, Any]:
        """Get API usage statistics.

        Returns:
            An API response payload.
        """
        await self._async_check_api_status_if_required()
        return await self._async_request("get", "stat")

    async def api_status(self) -> bool:
        """Get the current status of the API.

        Returns:
            True if the API is available, False if it is unavailable
        """
        resp = await self._async_request("get", "status")
        return cast(bool, resp["status"])

    async def uv_forecast(self) -> dict[str, Any]:
        """Get forecasted UV data.

        Returns:
            An API response payload.
        """
        await self._async_check_api_status_if_required()
        return await self._async_request("get", "forecast")

    async def uv_index(self) -> dict[str, Any]:
        """Get current UV data.

        Returns:
            An API response payload.
        """
        await self._async_check_api_status_if_required()
        return await self._async_request("get", "uv")

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
        await self._async_check_api_status_if_required()
        return await self._async_request(
            "get", "protection", params={"from": str(low), "to": str(high)}
        )
