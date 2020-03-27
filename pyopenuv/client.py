"""Define a client to interact with openuv.io."""
import asyncio
import logging
from typing import Awaitable, Optional

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from .errors import InvalidApiKeyError, RequestError

_LOGGER = logging.getLogger(__name__)

API_URL_SCAFFOLD: str = "https://api.openuv.io/api/v1"

DEFAULT_PROTECTION_HIGH: float = 3.5
DEFAULT_PROTECTION_LOW: float = 3.5
DEFAULT_TIMEOUT = 30


def _get_event_loop() -> asyncio.AbstractEventLoop:
    """Retrieve the event loop or creates a new one."""
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


class Client:
    """Define the client."""

    def __init__(
        self,
        api_key: str,
        latitude: float,
        longitude: float,
        *,
        altitude: float = 0.0,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
        session: Optional[ClientSession] = None,
        use_async: bool = False,
    ) -> None:
        """Initialize."""
        if session and not use_async:
            raise ValueError(
                "It doesn't make sense to use the session parameter without the "
                "use_async parameter"
            )

        self._api_key: str = api_key
        self._loop: Optional[asyncio.AbstractEventLoop] = event_loop
        self._session: ClientSession = session
        self._use_async = use_async
        self.altitude: str = str(altitude)
        self.latitude: str = str(latitude)
        self.longitude: str = str(longitude)

    def _wrap_future(self, coro: Awaitable):
        """Wrap a coroutine in a future and return or execute it."""
        if not self._loop:
            self._loop = _get_event_loop()

        future = asyncio.ensure_future(coro, loop=self._loop)
        if self._use_async:
            return future
        return self._loop.run_until_complete(future)

    async def async_request(
        self, method: str, endpoint: str, *, headers: dict = None, params: dict = None
    ) -> dict:
        """Make a request against OpenUV."""
        if not headers:
            headers = {}
        headers.update({"x-access-token": self._api_key})

        if not params:
            params = {}
        params.update(
            {"lat": self.latitude, "lng": self.longitude, "alt": self.altitude}
        )

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        try:
            async with session.request(
                method, f"{API_URL_SCAFFOLD}/{endpoint}", headers=headers, params=params
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data
        except asyncio.TimeoutError:
            raise RequestError("Request to endpoint timed out: {endpoint}")
        except ClientError as err:
            if any(code in str(err) for code in ("401", "403")):
                raise InvalidApiKeyError("Invalid API key")
            raise RequestError(
                f"Error requesting data from {endpoint}: {err}"
            ) from None
        finally:
            if not use_running_session:
                await session.close()

    def uv_forecast(self) -> dict:
        """Get forecasted UV data."""
        return self._wrap_future(self.async_request("get", "forecast"))

    def uv_index(self) -> dict:
        """Get current UV data."""
        return self._wrap_future(self.async_request("get", "uv"))

    def uv_protection_window(
        self, low: float = DEFAULT_PROTECTION_LOW, high: float = DEFAULT_PROTECTION_HIGH
    ) -> dict:
        """Get data on when a UV protection window is."""
        return self._wrap_future(
            self.async_request(
                "get", "protection", params={"from": str(low), "to": str(high)}
            )
        )
