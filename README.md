# ☀️  pyopenuv: A simple Python API for data from openuv.io

[![CI](https://github.com/bachya/pyopenuv/workflows/CI/badge.svg)](https://github.com/bachya/pyopenuv/actions)
[![PyPi](https://img.shields.io/pypi/v/pyopenuv.svg)](https://pypi.python.org/pypi/pyopenuv)
[![Version](https://img.shields.io/pypi/pyversions/pyopenuv.svg)](https://pypi.python.org/pypi/pyopenuv)
[![License](https://img.shields.io/pypi/l/pyopenuv.svg)](https://github.com/bachya/pyopenuv/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/pyopenuv/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/pyopenuv)
[![Maintainability](https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability)](https://codeclimate.com/github/bachya/pyopenuv/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`pyopenuv` is a simple Python library for retrieving UV-related information from
[openuv.io](https://openuv.io/).

# Installation

```python
pip install pyopenuv
```

# Python Versions

`pyopenuv` is currently supported on:

* Python 3.6
* Python 3.7
* Python 3.8

# API Key

You can get an API key from
[the OpenUV console](https://www.openuv.io/console).

# Usage

`pyopenuv` starts within an
[aiohttp](https://aiohttp.readthedocs.io/en/stable/) `ClientSession`:

```python
import asyncio

from aiohttp import ClientSession

from pyopenuv import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
      # YOUR CODE HERE


asyncio.get_event_loop().run_until_complete(main())
```

Create a client, initialize it, then get to it:

```python
import asyncio

from aiohttp import ClientSession

from pyopenuv import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
      client = pyopenuv.Client(
        "<OPENUV.IO API KEY>",
        "<LATITUDE>",
        "<LONGITUDE>",
        websession,
        altitude="<ALTITUDE>")

      # Get current UV index information:
      await client.uv_index()

      # Get forecasted UV information:
      await client.uv_forecast()

      # Get information on the window of time during which SPF protection
      # should be used:
      await client.uv_protection_window()


asyncio.get_event_loop().run_until_complete(main())
```

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/pyopenuv/issues)
  or [initiate a discussion on one](https://github.com/bachya/pyopenuv/issues/new).
2. [Fork the repository](https://github.com/bachya/pyopenuv/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `script/test`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!
