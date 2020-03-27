# ☀️  pyopenuv: A simple Python API for data from openuv.io

[![CI](https://github.com/bachya/pyopenuv/workflows/CI/badge.svg)](https://github.com/bachya/pyopenuv/actions)
[![PyPi](https://img.shields.io/pypi/v/pyopenuv.svg)](https://pypi.python.org/pypi/pyopenuv)
[![Version](https://img.shields.io/pypi/pyversions/pyopenuv.svg)](https://pypi.python.org/pypi/pyopenuv)
[![License](https://img.shields.io/pypi/l/pyopenuv.svg)](https://github.com/bachya/pyopenuv/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/pyopenuv/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/pyopenuv)
[![Maintainability](https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability)](https://codeclimate.com/github/bachya/pyopenuv/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`pyopenuv` is a simple Python library for retrieving UV-related information from
[openuv.io](https://openuv.io/). It supports both sync and async use cases.

- [Installation](#installation)
- [Python Versions](#python-versions)
- [API Key](#api-key)
- [Usage](#usage)
  * [Sync (Normal) Usage](#sync--normal--usage)
  * [Async Usage](#async-usage)
- [Contributing](#contributing)

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

## Sync (Normal) Usage

```python
from pyopenuv import Client
from pyopenuv.errors import OpenUvError

API_KEY = "<OPENUV_API_KEY>"
LATITUDE = 39.7974509
LONGITUDE = -104.8887227
ALTITUDE = 1609.3


client = Client(API_KEY, LATITUDE, LONGITUDE, altitude=ALTITUDE)

try:
    # Get current UV info:
    print(client.uv_index())

    # Get forecasted UV info:
    print(client.uv_forecast())

    # Get UV protection window:
    print(client.uv_protection_window())
except OpenUvError as err:
    print(f"There was an error: {err}")
```

## Async Usage

To use the library in an `asyncio`-friendly way, simply pass the `use_async` parameter when
creating a client. From there, the same methods can be used, but now as coroutines:

```python
import asyncio

from pyopenuv import Client
from pyopenuv.errors import OpenUvError

API_KEY = "<OPENUV_API_KEY>"
LATITUDE = 39.7974509
LONGITUDE = -104.8887227
ALTITUDE = 1609.3


async def main():
    client = Client(API_KEY, LATITUDE, LONGITUDE, altitude=ALTITUDE, use_async=True)

    try:
        # Get current UV info:
        print(await client.uv_index())

        # Get forecasted UV info:
        print(await client.uv_forecast())

        # Get UV protection window:
        print(await client.uv_protection_window())
    except OpenUvError as err:
        print(f"There was an error: {err}")


asyncio.get_event_loop().run_until_complete(main())
```

By default, the `asyncio`-friendly method creates a new connection to OpenUV with each
coroutine; this means that you won't get much in the way of runtime speed savings over
the normal, sync API. If you are calling a large number of coroutines (or merely want to
squeeze out every second of runtime savings possible), an
[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection
pooling:

```python
import asyncio

from aiohttp import ClientSession
from pyopenuv import Client
from pyopenuv.errors import OpenUvError

API_KEY = "<OPENUV_API_KEY>"
LATITUDE = 39.7974509
LONGITUDE = -104.8887227
ALTITUDE = 1609.3


async def main():
    async with ClientSession() as session:
        client = Client(
            API_KEY,
            LATITUDE,
            LONGITUDE,
            altitude=ALTITUDE,
            session=session,
            use_async=True,
        )

        try:
            # Get current UV info:
            print(await client.uv_index())

            # Get forecasted UV info:
            print(await client.uv_forecast())

            # Get UV protection window:
            print(await client.uv_protection_window())
        except OpenUvError as err:
            print(f"There was an error: {err}")


asyncio.get_event_loop().run_until_complete(main())
```

Check out the `[examples/`](https://github.com/bachya/pyopenuv/tree/dev/examples)
directory for more info.

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
