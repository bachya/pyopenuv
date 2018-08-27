"""Run an example script to quickly test."""
import asyncio

from aiohttp import ClientSession

from pyopenuv import Client
from pyopenuv.errors import OpenUvError


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        await run(websession)


async def run(websession: ClientSession):
    """Run."""
    try:
        # Create a client:
        client = Client(
            '<API_KEY>',
            39.7974509,
            -104.8887227,
            websession,
            altitude=1609.3)

        # Get current UV info:
        print('CURRENT UV DATA:')
        print(await client.uv_index())

        # Get forecasted UV info:
        print()
        print('FORECASTED UV DATA:')
        print(await client.uv_forecast())

        # Get UV protection window:
        print()
        print('UV PROTECTION WINDOW:')
        print(await client.uv_protection_window())
    except OpenUvError as err:
        print(err)


asyncio.get_event_loop().run_until_complete(main())
