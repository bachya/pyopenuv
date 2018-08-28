"""Define tests for the client object."""
# pylint: disable=redefined-outer-name
import json

import aiohttp
import pytest

from pyopenuv.util import validate_api_key


@pytest.fixture(scope='session')
def fixture_api_key_success():
    """Return a /protection response."""
    return {"result": []}


@pytest.mark.asyncio
async def test_api_key_success(
        aresponses, event_loop, fixture_api_key_success):
    """Test a good API key."""
    aresponses.add(
        'api.openuv.io', '/api/v1/forecast', 'get',
        aresponses.Response(
            text=json.dumps(fixture_api_key_success), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        result = await validate_api_key('12345', websession)
        assert result


@pytest.mark.asyncio
async def test_api_key_failure(aresponses, event_loop):
    """Test a good API key."""
    aresponses.add(
        'api.openuv.io', '/api/v1/forecast', 'get',
        aresponses.Response(
            text='', status=403))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        result = await validate_api_key('12345', websession)
        assert not result
