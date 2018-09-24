# ☀️  pyopenuv: A simple Python API for data from openuv.io

[![Travis CI](https://travis-ci.org/bachya/pyopenuv.svg?branch=master)](https://travis-ci.org/bachya/pyopenuv)
[![PyPi](https://img.shields.io/pypi/v/pyopenuv.svg)](https://pypi.python.org/pypi/pyopenuv)
[![Version](https://img.shields.io/pypi/pyversions/pyopenuv.svg)](https://pypi.python.org/pypi/pyopenuv)
[![License](https://img.shields.io/pypi/l/pyopenuv.svg)](https://github.com/bachya/pyopenuv/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/pyopenuv/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/pyopenuv)
[![Maintainability](https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability)](https://codeclimate.com/github/bachya/pyopenuv/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

pyopenuv is a simple Python library for retrieving UV-related information from
[openuv.io](https://openuv.io/).

# ☀️  Installation

```python
$ pip install pyopenuv
```

# ☀️  Usage

First, get an API key: https://www.openuv.io/console

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

# ☀️  Contributing

1. [Check for open features/bugs](https://github.com/bachya/pyopenuv/issues)
  or [initiate a discussion on one](https://github.com/bachya/pyopenuv/issues/new).
2. [Fork the repository](https://github.com/bachya/pyopenuv/fork).
3. Install the dev environment: `make init`.
4. Enter the virtual environment: `pipenv shell`
5. Code your new feature or bug fix.
6. Write a test that covers your new functionality.
7. Run tests and ensure 100% code coverage: `make coverage`
8. Add yourself to `AUTHORS.md`.
9. Submit a pull request!
