"""Define a client to interact with openuv.io."""
import asyncio
import logging
import sys
from typing import Any, Dict, Optional, cast

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError
import backoff

from .errors import InvalidApiKeyError, RequestError

_LOGGER = logging.getLogger(__name__)

API_URL_SCAFFOLD = "https://api.openuv.io/api/v1"

DEFAULT_PROTECTION_HIGH = 3.5
DEFAULT_PROTECTION_LOW = 3.5
DEFAULT_REQUEST_RETRIES = 3
DEFAULT_REQUEST_RETRY_INTERVAL = 3
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
        session: Optional[ClientSession] = None,
        request_retries: int = DEFAULT_REQUEST_RETRIES,
        request_retry_interval: int = DEFAULT_REQUEST_RETRY_INTERVAL,
    ) -> None:
        """Initialize."""
        self._api_key = api_key
        self._session = session
        self.altitude = str(altitude)
        self.latitude = str(latitude)
        self.longitude = str(longitude)

        # Implement a version of the request coroutine, but with backoff/retry logic:
        self.async_request = backoff.on_exception(
            backoff.constant,
            (asyncio.TimeoutError, ClientError),
            giveup=self._is_unauthorized_exception,
            interval=request_retry_interval,
            logger=_LOGGER,
            max_tries=request_retries,
            on_giveup=self._handle_on_giveup,
        )(self._async_request)

    async def _async_request(
        self, method: str, endpoint: str, **kwargs: Dict[str, str]
    ) -> Dict[str, Any]:
        """Make a request against OpenUV."""
        kwargs.setdefault("headers", {})
        kwargs["headers"]["x-access-token"] = self._api_key

        kwargs.setdefault("params", {})
        kwargs["params"]["lat"] = self.latitude
        kwargs["params"]["lng"] = self.longitude
        kwargs["params"]["alt"] = self.altitude

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        assert session

        async with session.request(
            method, f"{API_URL_SCAFFOLD}/{endpoint}", **kwargs
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()

        if not use_running_session:
            await session.close()

        return cast(Dict[str, Any], data)

    def _handle_on_giveup(self, _: Dict[str, Any]) -> None:
        """Determine what exception to raise upon giveup."""
        err_info = sys.exc_info()
        err = err_info[1].with_traceback(err_info[2])  # type: ignore

        if self._is_unauthorized_exception(err):
            raise InvalidApiKeyError("Invalid API key") from err
        raise RequestError(err) from err

    @staticmethod
    def _is_unauthorized_exception(err: BaseException) -> bool:
        """Return whether an exception represents an unauthorized error."""
        return isinstance(err, ClientError) and any(
            code in str(err) for code in ("401", "403")
        )

    async def uv_forecast(self) -> Dict[str, Any]:
        """Get forecasted UV data."""
        data = await self.async_request("get", "forecast")
        return cast(Dict[str, Any], data)

    async def uv_index(self) -> Dict[str, Any]:
        """Get current UV data."""
        data = await self.async_request("get", "uv")
        return cast(Dict[str, Any], data)

    async def uv_protection_window(
        self, low: float = DEFAULT_PROTECTION_LOW, high: float = DEFAULT_PROTECTION_HIGH
    ) -> Dict[str, Any]:
        """Get data on when a UV protection window is."""
        data = await self.async_request(
            "get", "protection", params={"from": str(low), "to": str(high)}
        )
        return cast(Dict[str, Any], data)
