"""Define a client to interact with openuv.io."""
import asyncio
import logging
from typing import Any, Dict, Optional, cast

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from .errors import InvalidApiKeyError, RequestError

_LOGGER = logging.getLogger(__name__)

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
        session: Optional[ClientSession] = None,
    ) -> None:
        """Initialize."""
        self._api_key = api_key
        self._session = session
        self.altitude = str(altitude)
        self.latitude = str(latitude)
        self.longitude = str(longitude)

    async def async_request(
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

        try:
            async with session.request(
                method, f"{API_URL_SCAFFOLD}/{endpoint}", **kwargs
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
        except asyncio.TimeoutError:
            raise RequestError("Request to endpoint timed out: {endpoint}") from None
        except ClientError as err:
            if any(code in str(err) for code in ("401", "403")):
                raise InvalidApiKeyError("Invalid API key") from err
            raise RequestError(f"Error requesting data from {endpoint}: {err}") from err
        finally:
            if not use_running_session:
                await session.close()

        return cast(Dict[str, Any], data)

    async def uv_forecast(self) -> Dict[str, Any]:
        """Get forecasted UV data."""
        return await self.async_request("get", "forecast")

    async def uv_index(self) -> Dict[str, Any]:
        """Get current UV data."""
        return await self.async_request("get", "uv")

    async def uv_protection_window(
        self, low: float = DEFAULT_PROTECTION_LOW, high: float = DEFAULT_PROTECTION_HIGH
    ) -> Dict[str, Any]:
        """Get data on when a UV protection window is."""
        return await self.async_request(
            "get", "protection", params={"from": str(low), "to": str(high)}
        )
