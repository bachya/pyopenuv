"""Define a client to interact with openuv.io."""
from aiohttp import ClientSession, client_exceptions

from .errors import InvalidApiKeyError, RequestError

API_URL_SCAFFOLD = 'https://api.openuv.io/api/v1'


class Client:
    """Define the client."""

    def __init__(
            self,
            api_key: str,
            latitude: float,
            longitude: float,
            websession: ClientSession,
            *,
            altitude: float = 0.0) -> None:
        """Initialize."""
        self._api_key = api_key
        self._websession = websession
        self.altitude = str(altitude)
        self.latitude = str(latitude)
        self.longitude = str(longitude)

    async def request(
            self,
            method: str,
            endpoint: str,
            *,
            headers: dict = None,
            params: dict = None) -> dict:
        """Make a request against air-matters.com."""
        url = '{0}/{1}'.format(API_URL_SCAFFOLD, endpoint)

        if not headers:
            headers = {}
        headers.update({'x-access-token': self._api_key})

        if not params:
            params = {}
        params.update({
            'lat': self.latitude,
            'lng': self.longitude,
            'alt': self.altitude
        })

        async with self._websession.request(method, url, headers=headers,
                                            params=params) as resp:
            try:
                resp.raise_for_status()
                return await resp.json(content_type=None)
            except client_exceptions.ClientError as err:
                if any(code in str(err) for code in ('401', '403')):
                    raise InvalidApiKeyError('Invalid API key')
                raise RequestError(
                    'Error requesting data from {0}: {1}'.format(
                        endpoint, err)) from None

    async def uv_forecast(self) -> dict:
        """Get forecasted UV data."""
        return await self.request('get', 'forecast')

    async def uv_index(self) -> dict:
        """Get current UV data."""
        return await self.request('get', 'uv')

    async def uv_protection_window(
            self, low: float = 3.5, high: float = 3.5) -> dict:
        """Get data on when a UV protection window is."""
        return await self.request(
            'get', 'protection', params={
                'from': str(low),
                'to': str(high)
            })
