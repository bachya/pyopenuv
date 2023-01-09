"""Define tests for the client object."""
from __future__ import annotations

import asyncio
import logging
from typing import Any
from unittest.mock import Mock, patch

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from pyopenuv import Client
from pyopenuv.errors import InvalidApiKeyError, RequestError
from tests.common import TEST_ALTITUDE, TEST_API_KEY, TEST_LATITUDE, TEST_LONGITUDE


@pytest.mark.asyncio
async def test_api_status(
    aresponses: ResponsesMockServer, api_status_response: dict[str, Any]
) -> None:
    """Test successfully retrieving the status of the API.

    Args:
        aresponses: An aresponses server.
        api_status_response: An API response payload.
    """
    aresponses.add(
        "api.openuv.io",
        "/api/v1/status",
        "get",
        response=aiohttp.web_response.json_response(api_status_response, status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(
            TEST_API_KEY,
            TEST_LATITUDE,
            TEST_LONGITUDE,
            altitude=TEST_ALTITUDE,
            session=session,
        )
        data = await client.api_status()
        assert data["status"] is True

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_bad_api_key(
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
async def test_custom_logger(
    aresponses: ResponsesMockServer,
    caplog: Mock,
    protection_window_response: dict[str, Any],
) -> None:
    """Test that a custom logger is used when provided to the client.

    Args:
        aresponses: An aresponses server.
        caplog: A mock logging utility.
        protection_window_response: An API response payload.
    """
    caplog.set_level(logging.DEBUG)
    custom_logger = logging.getLogger("custom")

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
            logger=custom_logger,
        )
        await client.uv_protection_window()
        assert any(
            record.name == "custom" and "Data received" in record.message
            for record in caplog.records
        )

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
        assert data["result"]["from_uv"] == 3.2509

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
    assert len(data["result"]) == 2

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
        assert len(data["result"]) == 2

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
        assert data["result"]["uv"] == 8.2342

    aresponses.assert_plan_strictly_followed()
