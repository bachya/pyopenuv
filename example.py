"""Run an example script to quickly test."""
import asyncio
import logging

from pyopenuv import Client
from pyopenuv.errors import OpenUvError

_LOGGER = logging.getLogger()


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)

    try:
        # Create a client:
        client = Client('<API_KEY>', 39.7974509, -104.8887227, altitude=1609.3)

        # Get current UV info:
        _LOGGER.info('CURRENT UV DATA: %s', await client.uv_index())

        # Get forecasted UV info:
        _LOGGER.info('FORECASTED UV DATA: %s', await client.uv_forecast())

        # Get UV protection window:
        _LOGGER.info(
            'UV PROTECTION WINDOW: %s', await client.uv_protection_window())
    except OpenUvError as err:
        print(err)


asyncio.get_event_loop().run_until_complete(main())
