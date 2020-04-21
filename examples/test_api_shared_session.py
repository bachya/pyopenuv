"""Run an example script to quickly test."""
import asyncio
import logging
import time

from aiohttp import ClientSession

from pyopenuv import Client
from pyopenuv.errors import OpenUvError

_LOGGER = logging.getLogger(__name__)

API_KEY = "<OPENUV_API_KEY>"
LATITUDE = 39.7974509
LONGITUDE = -104.8887227
ALTITUDE = 1609.3


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.DEBUG)

    async with ClientSession() as session:
        client = Client(
            API_KEY, LATITUDE, LONGITUDE, altitude=ALTITUDE, session=session,
        )

        start = time.time()

        try:
            # Get current UV info:
            _LOGGER.info("CURRENT UV DATA:")
            _LOGGER.info(await client.uv_index())

            # Get forecasted UV info:
            _LOGGER.info("FORECASTED UV DATA:")
            _LOGGER.info(await client.uv_forecast())

            # Get UV protection window:
            _LOGGER.info("UV PROTECTION WINDOW:")
            _LOGGER.info(await client.uv_protection_window())
        except OpenUvError as err:
            _LOGGER.info(err)

    end = time.time()

    _LOGGER.info("Execution time: %s seconds", end - start)


asyncio.run(main())
