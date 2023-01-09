"""Define dynamic text fixtures."""
from __future__ import annotations

import json
from typing import Any, cast

import pytest

from .common import load_fixture


@pytest.fixture(name="api_status_response", scope="session")
def api_status_response_fixture() -> dict[str, Any]:
    """Define a fixture to return an API status response.

    Returns:
        An API response payload.
    """
    return cast(dict[str, Any], json.loads(load_fixture("api_status_response.json")))


@pytest.fixture(name="error_invalid_api_key_response", scope="session")
def error_invalid_api_key_response_fixture() -> dict[str, Any]:
    """Define a fixture to return an invalid API key error response.

    Returns:
        An API response payload.
    """
    return cast(
        dict[str, Any], json.loads(load_fixture("error_invalid_api_key_response.json"))
    )


@pytest.fixture(name="protection_window_response", scope="session")
def protection_window_response_fixture() -> dict[str, Any]:
    """Define a fixture to return a protection window response.

    Returns:
        An API response payload.
    """
    return cast(
        dict[str, Any], json.loads(load_fixture("protection_window_response.json"))
    )


@pytest.fixture(name="uv_forecast_response", scope="session")
def uv_forecast_response_fixture() -> dict[str, Any]:
    """Define a fixture to return an UV forecast response.

    Returns:
        An API response payload.
    """
    return cast(dict[str, Any], json.loads(load_fixture("uv_forecast_response.json")))


@pytest.fixture(name="uv_index_response", scope="session")
def uv_index_response_fixture() -> dict[str, Any]:
    """Define a fixture to return an UV index response.

    Returns:
        An API response payload.
    """
    return cast(dict[str, Any], json.loads(load_fixture("uv_index_response.json")))
