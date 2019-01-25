"""Define tests for the client object."""
# pylint: disable=redefined-outer-name,unused-import
import json

import aiohttp
import pytest

from pyopenuv import Client
from pyopenuv.errors import InvalidApiKeyError, RequestError

from .const import TEST_ALTITUDE, TEST_API_KEY, TEST_LATITUDE, TEST_LONGITUDE
from .fixtures.client import *  # noqa


@pytest.mark.asyncio
async def test_bad_api_key(aresponses):
    """Test the that the property exception is raised with a bad API key."""
    aresponses.add(
        'api.openuv.io', '/api/v1/protection', 'get',
        aresponses.Response(text='', status=403))

    with pytest.raises(InvalidApiKeyError):
        client = Client(
            TEST_API_KEY,
            TEST_LATITUDE,
            TEST_LONGITUDE,
            altitude=TEST_ALTITUDE)
        await client.uv_protection_window()


@pytest.mark.asyncio
async def test_bad_request(aresponses):
    """Test that the proper exception is raised during a bad request."""
    aresponses.add(
        'api.openuv.io', '/api/v1/bad_endpoint', 'get',
        aresponses.Response(text='', status=500))

    with pytest.raises(RequestError):
        client = Client(
            TEST_API_KEY,
            TEST_LATITUDE,
            TEST_LONGITUDE,
            altitude=TEST_ALTITUDE)
        await client.request('get', 'bad_endpoint')


@pytest.mark.asyncio
async def test_create():
    """Test the creation of a client."""
    client = Client(
        TEST_API_KEY, TEST_LATITUDE, TEST_LONGITUDE, altitude=TEST_ALTITUDE)

    assert client.altitude == TEST_ALTITUDE
    assert client.latitude == TEST_LATITUDE
    assert client.longitude == TEST_LONGITUDE


@pytest.mark.asyncio
async def test_protection_window(aresponses, fixture_protection_window):
    """Test successfully retrieving the protection window."""
    aresponses.add(
        'api.openuv.io', '/api/v1/protection', 'get',
        aresponses.Response(
            text=json.dumps(fixture_protection_window), status=200))

    client = Client(
        TEST_API_KEY,
        TEST_LATITUDE,
        TEST_LONGITUDE,
        altitude=TEST_ALTITUDE)

    data = await client.uv_protection_window()
    assert data['result']['from_uv'] == 3.2509


@pytest.mark.asyncio
async def test_uv_forecast(aresponses, fixture_uv_forecast):
    """Test successfully retrieving UV forecast info."""
    aresponses.add(
        'api.openuv.io', '/api/v1/forecast', 'get',
        aresponses.Response(text=json.dumps(fixture_uv_forecast), status=200))

    client = Client(
        TEST_API_KEY,
        TEST_LATITUDE,
        TEST_LONGITUDE,
        altitude=TEST_ALTITUDE)

    data = await client.uv_forecast()
    assert len(data['result']) == 2


@pytest.mark.asyncio
async def test_uv_index(aresponses, fixture_uv_index):
    """Test successfully retrieving UV index info."""
    aresponses.add(
        'api.openuv.io', '/api/v1/uv', 'get',
        aresponses.Response(text=json.dumps(fixture_uv_index), status=200))

    client = Client(
        TEST_API_KEY,
        TEST_LATITUDE,
        TEST_LONGITUDE,
        altitude=TEST_ALTITUDE)

    data = await client.uv_index()
    assert data['result']['uv'] == 8.2342
