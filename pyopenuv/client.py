"""Define a client to interact with openuv.io."""
import logging

from aiohttp import ClientSession, client_exceptions

from .errors import InvalidApiKeyError, RequestError

_LOGGER = logging.getLogger(__name__)

API_URL_SCAFFOLD: str = "https://api.openuv.io/api/v1"

DEFAULT_PROTECTION_HIGH: float = 3.5
DEFAULT_PROTECTION_LOW: float = 3.5


class Client:
    """Define the client."""

    def __init__(
        self,
        api_key: str,
        latitude: float,
        longitude: float,
        websession: ClientSession,
        *,
        altitude: float = 0.0,
    ) -> None:
        """Initialize."""
        self._api_key: str = api_key
        self._websession: ClientSession = websession
        self.altitude: str = str(altitude)
        self.latitude: str = str(latitude)
        self.longitude: str = str(longitude)

    async def request(
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

        async with self._websession.request(
            method, f"{API_URL_SCAFFOLD}/{endpoint}", headers=headers, params=params
        ) as resp:
            try:
                resp.raise_for_status()
                data = await resp.json(content_type=None)
                _LOGGER.info(data)
                return data
            except client_exceptions.ClientError as err:
                _LOGGER.debug(err)
                if any(code in str(err) for code in ("401", "403")):
                    raise InvalidApiKeyError("Invalid API key")
                raise RequestError(
                    f"Error requesting data from {endpoint}: {err}"
                ) from None

    async def uv_forecast(self) -> dict:
        """Get forecasted UV data."""
        return await self.request("get", "forecast")

    async def uv_index(self) -> dict:
        """Get current UV data."""
        return await self.request("get", "uv")

    async def uv_protection_window(
        self, low: float = DEFAULT_PROTECTION_LOW, high: float = DEFAULT_PROTECTION_HIGH
    ) -> dict:
        """Get data on when a UV protection window is."""
        return await self.request(
            "get", "protection", params={"from": str(low), "to": str(high)}
        )
