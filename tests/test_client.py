"""Define tests for the client object."""
import aiohttp
import pytest

from pyopenuv import Client
from pyopenuv.errors import InvalidApiKeyError, RequestError

from .common import (
    TEST_ALTITUDE,
    TEST_API_KEY,
    TEST_LATITUDE,
    TEST_LONGITUDE,
    load_fixture,
)


@pytest.mark.asyncio
async def test_bad_api_key(aresponses):
    """Test the that the proper exception is raised with a bad API key."""
    aresponses.add(
        "api.openuv.io",
        "/api/v1/protection",
        "get",
        aresponses.Response(text="", status=403),
    )

    with pytest.raises(InvalidApiKeyError):
        async with aiohttp.ClientSession() as websession:
            client = Client(
                TEST_API_KEY,
                TEST_LATITUDE,
                TEST_LONGITUDE,
                websession,
                altitude=TEST_ALTITUDE,
            )
            await client.uv_protection_window()


@pytest.mark.asyncio
async def test_bad_request(aresponses):
    """Test that the proper exception is raised during a bad request."""
    aresponses.add(
        "api.openuv.io",
        "/api/v1/bad_endpoint",
        "get",
        aresponses.Response(text="", status=500),
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession() as websession:
            client = Client(
                TEST_API_KEY,
                TEST_LATITUDE,
                TEST_LONGITUDE,
                websession,
                altitude=TEST_ALTITUDE,
            )
            await client.request("get", "bad_endpoint")


@pytest.mark.asyncio
async def test_create():
    """Test the creation of a client."""
    async with aiohttp.ClientSession() as websession:
        client = Client(
            TEST_API_KEY,
            TEST_LATITUDE,
            TEST_LONGITUDE,
            websession,
            altitude=TEST_ALTITUDE,
        )
        assert client.altitude == TEST_ALTITUDE
        assert client.latitude == TEST_LATITUDE
        assert client.longitude == TEST_LONGITUDE


@pytest.mark.asyncio
async def test_protection_window(aresponses):
    """Test successfully retrieving the protection window."""
    aresponses.add(
        "api.openuv.io",
        "/api/v1/protection",
        "get",
        aresponses.Response(
            text=load_fixture("protection_window_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as websession:
        client = Client(
            TEST_API_KEY,
            TEST_LATITUDE,
            TEST_LONGITUDE,
            websession,
            altitude=TEST_ALTITUDE,
        )
        data = await client.uv_protection_window()
        assert data["result"]["from_uv"] == 3.2509


@pytest.mark.asyncio
async def test_uv_forecast(aresponses):
    """Test successfully retrieving UV forecast info."""
    aresponses.add(
        "api.openuv.io",
        "/api/v1/forecast",
        "get",
        aresponses.Response(text=load_fixture("uv_forecast_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as websession:
        client = Client(
            TEST_API_KEY,
            TEST_LATITUDE,
            TEST_LONGITUDE,
            websession,
            altitude=TEST_ALTITUDE,
        )
        data = await client.uv_forecast()
        assert len(data["result"]) == 2


@pytest.mark.asyncio
async def test_uv_index(aresponses):
    """Test successfully retrieving UV index info."""
    aresponses.add(
        "api.openuv.io",
        "/api/v1/uv",
        "get",
        aresponses.Response(text=load_fixture("uv_index_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as websession:
        client = Client(
            TEST_API_KEY,
            TEST_LATITUDE,
            TEST_LONGITUDE,
            websession,
            altitude=TEST_ALTITUDE,
        )
        data = await client.uv_index()
        assert data["result"]["uv"] == 8.2342
