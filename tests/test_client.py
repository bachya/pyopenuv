"""Define tests for the client object."""
# pylint: disable=protected-access
import asyncio

import aiohttp
from asynctest import patch
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
        async with aiohttp.ClientSession() as session:
            client = Client(
                TEST_API_KEY,
                TEST_LATITUDE,
                TEST_LONGITUDE,
                altitude=TEST_ALTITUDE,
                session=session,
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
        async with aiohttp.ClientSession() as session:
            client = Client(
                TEST_API_KEY,
                TEST_LATITUDE,
                TEST_LONGITUDE,
                altitude=TEST_ALTITUDE,
                session=session,
            )
            await client.async_request("get", "bad_endpoint")


@pytest.mark.asyncio
async def test_protection_window(aresponses):
    """Test successfully retrieving the protection window."""
    aresponses.add(
        "api.openuv.io",
        "/api/v1/protection",
        "get",
        aresponses.Response(
            text=load_fixture("protection_window_response.json"),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(
            TEST_API_KEY,
            TEST_LATITUDE,
            TEST_LONGITUDE,
            altitude=TEST_ALTITUDE,
            session=session,
        )
        data = await client.uv_protection_window()
        assert data["result"]["from_uv"] == 3.2509


@pytest.mark.asyncio
async def test_timeout():
    """Test that a timeout raises an exception."""
    async with aiohttp.ClientSession() as session:
        client = Client(
            TEST_API_KEY,
            TEST_LATITUDE,
            TEST_LONGITUDE,
            altitude=TEST_ALTITUDE,
            session=session,
        )

        with patch("aiohttp.ClientSession.request", side_effect=asyncio.TimeoutError):
            with pytest.raises(RequestError):
                await client.uv_forecast()


@pytest.mark.asyncio
async def test_session_from_scratch(aresponses):
    """Test that an aiohttp ClientSession is created on the fly if needed."""
    aresponses.add(
        "api.openuv.io",
        "/api/v1/forecast",
        "get",
        aresponses.Response(
            text=load_fixture("uv_forecast_response.json"),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    client = Client(TEST_API_KEY, TEST_LATITUDE, TEST_LONGITUDE, altitude=TEST_ALTITUDE)
    data = await client.uv_forecast()
    assert len(data["result"]) == 2


@pytest.mark.asyncio
async def test_uv_forecast(aresponses):
    """Test successfully retrieving UV forecast info."""
    aresponses.add(
        "api.openuv.io",
        "/api/v1/forecast",
        "get",
        aresponses.Response(
            text=load_fixture("uv_forecast_response.json"),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(
            TEST_API_KEY,
            TEST_LATITUDE,
            TEST_LONGITUDE,
            altitude=TEST_ALTITUDE,
            session=session,
        )
        data = await client.uv_forecast()
        assert len(data["result"]) == 2


@pytest.mark.asyncio
async def test_uv_index_async(aresponses):
    """Test successfully retrieving UV index info (async)."""
    aresponses.add(
        "api.openuv.io",
        "/api/v1/uv",
        "get",
        aresponses.Response(
            text=load_fixture("uv_index_response.json"),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(
            TEST_API_KEY,
            TEST_LATITUDE,
            TEST_LONGITUDE,
            altitude=TEST_ALTITUDE,
            session=session,
        )
        data = await client.uv_index()
        assert data["result"]["uv"] == 8.2342
