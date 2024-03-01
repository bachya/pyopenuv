"""Define common test utilities."""

from __future__ import annotations

import os

TEST_ALTITUDE = 1609.3
TEST_API_KEY = "12345"
TEST_LATITUDE = 51.528308
TEST_LONGITUDE = -0.3817803


def load_fixture(filename: str) -> str:
    """Load a fixture.

    Args:
        filename: The filename of the fixtures/ file to load.

    Returns:
        A string containing the contents of the file.
    """
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
