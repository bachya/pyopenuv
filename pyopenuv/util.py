"""Define utilities."""

from aiohttp import ClientSession


async def validate_api_key(api_key: str, websession: ClientSession) -> bool:
    """Return whether an API key is valid."""
    async with websession.request('get',
                                  'https://api.openuv.io/api/v1/forecast',
                                  headers={'x-access-token': api_key}) as resp:
        return resp.status == 200
