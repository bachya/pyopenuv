# ☀️ pyopenuv: A simple Python API for data from openuv.io

[![CI][ci-badge]][ci]
[![PyPI][pypi-badge]][pypi]
[![Version][version-badge]][version]
[![License][license-badge]][license]
[![Code Coverage][codecov-badge]][codecov]
[![Maintainability][maintainability-badge]][maintainability]

<a href="https://www.buymeacoffee.com/bachya1208P" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

`pyopenuv` is a simple Python library for retrieving UV-related information from
[openuv.io][openuv].

- [Installation](#installation)
- [Python Versions](#python-versions)
- [API Key](#api-key)
- [Usage](#usage)
- [Contributing](#contributing)

# Installation

```bash
pip install pyopenuv
```

# Python Versions

`pyopenuv` is currently supported on:

- Python 3.9
- Python 3.10
- Python 3.11

# API Key

You can get an API key from [the OpenUV console][openuv-console].

# Usage

```python
import asyncio

from pyopenuv import Client
from pyopenuv.errors import OpenUvError


async def main():
    client = Client(
        "<OPENUV_API_KEY>", "<LATITUDE>", "<LONGITUDE>", altitude="<ALTITUDE>"
    )

    try:
        # Get the current status of the OpenUV API:
        print(await client.api_status())
        # >>> True

        # Get current UV info:
        print(await client.uv_index())
        # >>> { "result": { ... } }

        # Get forecasted UV info:
        print(await client.uv_forecast())
        # >>> { "result": { ... } }

        # Get UV protection window:
        print(await client.uv_protection_window())
        # >>> { "result": { ... } }

        # Get API usage info/statistics:
        print(await client.api_statistics())
        # >>> { "result": { ... } }
    except OpenUvError as err:
        print(f"There was an error: {err}")


asyncio.run(main())
```

## Checking API Status Before Requests

If you would prefer to not call `api_status` manually, you can configure the `Client` object
to automatically check the status of the OpenUV API before executing any of the API
methods—simply pass the `check_status_before_request` parameter:

```python
import asyncio

from pyopenuv import Client
from pyopenuv.errors import ApiUnavailableError, OpenUvError


async def main():
    client = Client(
        "<OPENUV_API_KEY>",
        "<LATITUDE>",
        "<LONGITUDE>",
        altitude="<ALTITUDE>",
        check_status_before_request=True,
    )

    try:
        print(await client.uv_index())
    except ApiUnavailableError:
        print("The API is unavailable")
    except OpenUvError as err:
        print(f"There was an error: {err}")


asyncio.run(main())
```

## Connection Pooling

By default, the library creates a new connection to OpenUV with each coroutine. If you
are calling a large number of coroutines (or merely want to squeeze out every second of
runtime savings possible), an [`aiohttp`][aiohttp] `ClientSession` can be used for
connection pooling:

```python
import asyncio

from aiohttp import ClientSession
from pyopenuv import Client
from pyopenuv.errors import OpenUvError


async def main():
    async with ClientSession() as session:
        client = Client(
            "<OPENUV_API_KEY>",
            "<LATITUDE>",
            "<LONGITUDE>",
            altitude="<ALTITUDE>",
            session=session,
        )

        try:
            print(await client.uv_index())
        except OpenUvError as err:
            print(f"There was an error: {err}")


asyncio.run(main())
```

# Contributing

Thanks to all of [our contributors][contributors] so far!

1. [Check for open features/bugs][issues] or [initiate a discussion on one][new-issue].
2. [Fork the repository][fork].
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix on a new branch.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `poetry run pytest --cov pyopenuv tests`
9. Update `README.md` with any new documentation.
10. Submit a pull request!

[aiohttp]: https://github.com/aio-libs/aiohttp
[ci-badge]: https://github.com/bachya/pyopenuv/workflows/CI/badge.svg
[ci]: https://github.com/bachya/pyopenuv/actions
[codecov-badge]: https://codecov.io/gh/bachya/pyopenuv/branch/dev/graph/badge.svg
[codecov]: https://codecov.io/gh/bachya/pyopenuv
[contributors]: https://github.com/bachya/pyopenuv/graphs/contributors
[fork]: https://github.com/bachya/pyopenuv/fork
[issues]: https://github.com/bachya/pyopenuv/issues
[license-badge]: https://img.shields.io/pypi/l/pyopenuv.svg
[license]: https://github.com/bachya/pyopenuv/blob/main/LICENSE
[maintainability-badge]: https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability
[maintainability]: https://codeclimate.com/github/bachya/pyopenuv/maintainability
[new-issue]: https://github.com/bachya/pyopenuv/issues/new
[new-issue]: https://github.com/bachya/pyopenuv/issues/new
[openuv]: https://openuv.io/
[openuv-console]: https://www.openuv.io/console
[pypi-badge]: https://img.shields.io/pypi/v/pyopenuv.svg
[pypi]: https://pypi.python.org/pypi/pyopenuv
[version-badge]: https://img.shields.io/pypi/pyversions/pyopenuv.svg
[version]: https://pypi.python.org/pypi/pyopenuv
