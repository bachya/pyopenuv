"""Define tests for the client object."""
from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import patch

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from pyopenuv import Client
from pyopenuv.errors import (
    ApiUnavailableError,
    InvalidApiKeyError,
    RateLimitExceededError,
    RequestError,
)
from tests.common import TEST_ALTITUDE, TEST_API_KEY, TEST_LATITUDE, TEST_LONGITUDE


@pytest.mark.asyncio
async def test_api_statistics(
    aresponses: ResponsesMockServer, api_statistics_response: dict[str, Any]
) -> None:
    """Test successfully retrieving API usage statistics.

    Args:
        aresponses: An aresponses server.
        api_statistics_response: An API response payload.
    """
    aresponses.add(
        "api.openuv.io",
        "/api/v1/stat",
        "get",
        response=aiohttp.web_response.json_response(
            api_statistics_response, status=200
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
        data = await client.api_statistics()
        assert data == {
            "result": {
                "requests_today": 25,
                "requests_yesterday": 14,
                "requests_month": 146,
                "requests_last_month": 446,
                "cost_today": 0,
                "cost_yesterday": 0,
                "cost_month": 0.024,
                "cost_last_month": 0,
            }
        }

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_bad_request(aresponses: ResponsesMockServer) -> None:
    """Test that the proper exception is raised during a bad request.

    Args:
        aresponses: An aresponses server.
    """
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
            await client._async_request(  # pylint: disable=protected-access
                "get", "bad_endpoint"
            )

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_error_invalid_api_key(
    aresponses: ResponsesMockServer, error_invalid_api_key_response: dict[str, Any]
) -> None:
    """Test the that the proper exception is raised with a bad API key.

    Args:
        aresponses: An aresponses server.
        error_invalid_api_key_response: An API response payload.
    """
    aresponses.add(
        "api.openuv.io",
        "/api/v1/protection",
        "get",
        response=aiohttp.web_response.json_response(
            error_invalid_api_key_response, status=403
        ),
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

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_error_rate_limited(
    aresponses: ResponsesMockServer, error_rate_limit_response: dict[str, Any]
) -> None:
    """Test the that the proper exception is raised when the rate limit is reached.

    Args:
        aresponses: An aresponses server.
        error_rate_limit_response: An API response payload.
    """
    aresponses.add(
        "api.openuv.io",
        "/api/v1/protection",
        "get",
        response=aiohttp.web_response.json_response(
            error_rate_limit_response, status=403
        ),
    )

    with pytest.raises(RateLimitExceededError):
        async with aiohttp.ClientSession() as session:
            client = Client(
                TEST_API_KEY,
                TEST_LATITUDE,
                TEST_LONGITUDE,
                altitude=TEST_ALTITUDE,
                session=session,
            )
            await client.uv_protection_window()

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_protection_window(
    aresponses: ResponsesMockServer, protection_window_response: dict[str, Any]
) -> None:
    """Test successfully retrieving the protection window.

    Args:
        aresponses: An aresponses server.
        protection_window_response: An API response payload.
    """
    aresponses.add(
        "api.openuv.io",
        "/api/v1/protection",
        "get",
        response=aiohttp.web_response.json_response(
            protection_window_response, status=200
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
        assert data == {
            "result": {
                "from_time": "2018-07-30T15:17:49.750Z",
                "from_uv": 3.2509,
                "to_time": "2018-07-30T22:47:49.750Z",
                "to_uv": 3.6483,
            }
        }

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_session_from_scratch(
    aresponses: ResponsesMockServer, uv_forecast_response: dict[str, Any]
) -> None:
    """Test that an aiohttp ClientSession is created on the fly if needed.

    Args:
        aresponses: An aresponses server.
        uv_forecast_response: An API response payload.
    """
    aresponses.add(
        "api.openuv.io",
        "/api/v1/forecast",
        "get",
        response=aiohttp.web_response.json_response(uv_forecast_response, status=200),
    )

    client = Client(TEST_API_KEY, TEST_LATITUDE, TEST_LONGITUDE, altitude=TEST_ALTITUDE)
    data = await client.uv_forecast()
    assert data == {
        "result": [
            {
                "uv": 0,
                "uv_time": "2018-07-30T11:57:49.750Z",
                "sun_position": {
                    "azimuth": -2.0081567900835937,
                    "altitude": -0.011856950133816461,
                },
            },
            {
                "uv": 0.2446,
                "uv_time": "2018-07-30T12:57:49.750Z",
                "sun_position": {
                    "azimuth": -1.845666592871966,
                    "altitude": 0.1764062658258758,
                },
            },
        ]
    }

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_timeout() -> None:
    """Test that a timeout raises an exception."""
    async with aiohttp.ClientSession() as session:
        client = Client(
            TEST_API_KEY,
            TEST_LATITUDE,
            TEST_LONGITUDE,
            altitude=TEST_ALTITUDE,
            session=session,
        )

        with patch(
            "aiohttp.ClientSession.request", side_effect=asyncio.TimeoutError
        ), pytest.raises(RequestError):
            await client.uv_forecast()


@pytest.mark.asyncio
async def test_uv_forecast(
    aresponses: ResponsesMockServer, uv_forecast_response: dict[str, Any]
) -> None:
    """Test successfully retrieving UV forecast info.

    Args:
        aresponses: An aresponses server.
        uv_forecast_response: An API response payload.
    """
    aresponses.add(
        "api.openuv.io",
        "/api/v1/forecast",
        "get",
        response=aiohttp.web_response.json_response(uv_forecast_response, status=200),
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
        assert data == {
            "result": [
                {
                    "uv": 0,
                    "uv_time": "2018-07-30T11:57:49.750Z",
                    "sun_position": {
                        "azimuth": -2.0081567900835937,
                        "altitude": -0.011856950133816461,
                    },
                },
                {
                    "uv": 0.2446,
                    "uv_time": "2018-07-30T12:57:49.750Z",
                    "sun_position": {
                        "azimuth": -1.845666592871966,
                        "altitude": 0.1764062658258758,
                    },
                },
            ]
        }

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_uv_index(
    aresponses: ResponsesMockServer, uv_index_response: dict[str, Any]
) -> None:
    """Test successfully retrieving UV index info.

    Args:
        aresponses: An aresponses server.
        uv_index_response: An API response payload.
    """
    aresponses.add(
        "api.openuv.io",
        "/api/v1/uv",
        "get",
        response=aiohttp.web_response.json_response(uv_index_response, status=200),
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
        assert data == {
            "result": {
                "uv": 8.2342,
                "uv_time": "2018-07-30T20:53:06.302Z",
                "uv_max": 10.3335,
                "uv_max_time": "2018-07-30T19:07:11.505Z",
                "ozone": 300.7,
                "ozone_time": "2018-07-30T18:07:04.466Z",
                "safe_exposure_time": {
                    "st1": 20,
                    "st2": 24,
                    "st3": 32,
                    "st4": 40,
                    "st5": 65,
                    "st6": 121,
                },
                "sun_info": {
                    "sun_times": {
                        "solarNoon": "2018-07-30T19:07:11.505Z",
                        "nadir": "2018-07-30T07:07:11.505Z",
                        "sunrise": "2018-07-30T11:57:49.750Z",
                        "sunset": "2018-07-31T02:16:33.259Z",
                        "sunriseEnd": "2018-07-30T12:00:53.253Z",
                        "sunsetStart": "2018-07-31T02:13:29.756Z",
                        "dawn": "2018-07-30T11:27:27.911Z",
                        "dusk": "2018-07-31T02:46:55.099Z",
                        "nauticalDawn": "2018-07-30T10:50:01.621Z",
                        "nauticalDusk": "2018-07-31T03:24:21.389Z",
                        "nightEnd": "2018-07-30T10:08:47.846Z",
                        "night": "2018-07-31T04:05:35.163Z",
                        "goldenHourEnd": "2018-07-30T12:36:14.026Z",
                        "goldenHour": "2018-07-31T01:38:08.983Z",
                    },
                    "sun_position": {
                        "azimuth": 0.9567419441563509,
                        "altitude": 1.0235714275875594,
                    },
                },
            }
        }

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_uv_index_with_api_status_check_first(
    aresponses: ResponsesMockServer,
    api_status_response: dict[str, Any],
    uv_index_response: dict[str, Any],
) -> None:
    """Test successfully retrieving UV index info after confirming the API status.

    Args:
        aresponses: An aresponses server.
        api_status_response: An API response payload.
        uv_index_response: An API response payload.
    """
    aresponses.add(
        "api.openuv.io",
        "/api/v1/status",
        "get",
        response=aiohttp.web_response.json_response(api_status_response, status=200),
    )
    aresponses.add(
        "api.openuv.io",
        "/api/v1/uv",
        "get",
        response=aiohttp.web_response.json_response(uv_index_response, status=200),
    )
    aresponses.add(
        "api.openuv.io",
        "/api/v1/status",
        "get",
        response=aiohttp.web_response.json_response({"status": False}, status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(
            TEST_API_KEY,
            TEST_LATITUDE,
            TEST_LONGITUDE,
            altitude=TEST_ALTITUDE,
            session=session,
            check_status_before_request=True,
        )

        # Test getting the data with a successful API status check:
        data = await client.uv_index()
        assert data == {
            "result": {
                "uv": 8.2342,
                "uv_time": "2018-07-30T20:53:06.302Z",
                "uv_max": 10.3335,
                "uv_max_time": "2018-07-30T19:07:11.505Z",
                "ozone": 300.7,
                "ozone_time": "2018-07-30T18:07:04.466Z",
                "safe_exposure_time": {
                    "st1": 20,
                    "st2": 24,
                    "st3": 32,
                    "st4": 40,
                    "st5": 65,
                    "st6": 121,
                },
                "sun_info": {
                    "sun_times": {
                        "solarNoon": "2018-07-30T19:07:11.505Z",
                        "nadir": "2018-07-30T07:07:11.505Z",
                        "sunrise": "2018-07-30T11:57:49.750Z",
                        "sunset": "2018-07-31T02:16:33.259Z",
                        "sunriseEnd": "2018-07-30T12:00:53.253Z",
                        "sunsetStart": "2018-07-31T02:13:29.756Z",
                        "dawn": "2018-07-30T11:27:27.911Z",
                        "dusk": "2018-07-31T02:46:55.099Z",
                        "nauticalDawn": "2018-07-30T10:50:01.621Z",
                        "nauticalDusk": "2018-07-31T03:24:21.389Z",
                        "nightEnd": "2018-07-30T10:08:47.846Z",
                        "night": "2018-07-31T04:05:35.163Z",
                        "goldenHourEnd": "2018-07-30T12:36:14.026Z",
                        "goldenHour": "2018-07-31T01:38:08.983Z",
                    },
                    "sun_position": {
                        "azimuth": 0.9567419441563509,
                        "altitude": 1.0235714275875594,
                    },
                },
            }
        }

        # Test raising when the API status check fails on a second attempt:
        with pytest.raises(ApiUnavailableError):
            data = await client.uv_index()

    aresponses.assert_plan_strictly_followed()
