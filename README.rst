☀️  pyopenuv: A simple Python API for data from openuv.io
========================================================

.. image:: https://travis-ci.org/bachya/pyopenuv.svg?branch=master
  :target: https://travis-ci.org/bachya/pyopenuv

.. image:: https://img.shields.io/pypi/v/pyopenuv.svg
  :target: https://pypi.python.org/pypi/pyopenuv

.. image:: https://img.shields.io/pypi/pyversions/pyopenuv.svg
  :target: https://pypi.python.org/pypi/pyopenuv

.. image:: https://img.shields.io/pypi/l/pyopenuv.svg
  :target: https://github.com/bachya/pyopenuv/blob/master/LICENSE

.. image:: https://codecov.io/gh/bachya/pyopenuv/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/bachya/pyopenuv

.. image:: https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability
   :target: https://codeclimate.com/github/bachya/pyopenuv/maintainability

.. image:: https://img.shields.io/badge/SayThanks-!-1EAEDB.svg
  :target: https://saythanks.io/to/bachya

pyopenuv is a simple Python library for retrieving UV-related information from
`openuv.io <https://openuv.io/>`_.

☀️  Installation
===============

.. code-block:: bash

  $ pip install pyopenuv

☀️  Usage
========

.. code-block:: python

  import pyopenuv

pyopenuv starts within an
`aiohttp <https://aiohttp.readthedocs.io/en/stable/>`_ :code:`ClientSession`:

.. code-block:: python

  import asyncio

  from aiohttp import ClientSession

  from pyopenuv import Client


  async def main() -> None:
      """Create the aiohttp session and run the example."""
      async with ClientSession() as websession:
          await run(websession)


  async def run(websession):
      """Run."""
      # YOUR CODE HERE

  asyncio.get_event_loop().run_until_complete(main())

Get an API key: `https://www.openuv.io/console <https://www.openuv.io/console>`_

Create a client and initialize it:

.. code-block:: python

  client = pyopenuv.Client(
    '<OPENUV.IO API KEY>',
    '<LATITUDE>',
    '<LONGITUDE>',
    websession,
    altitude='<ALTITUDE>')

Then, get to it!

.. code-block:: python

  # Get current UV index information:
  await client.uv_index()

  # Get forecasted UV information:
  await client.uv_forecast()

  # Get information on the window of time during which SPF protection should
  # be used:
  await client.uv_protection_window()


☀️  Contributing
===============

#. `Check for open features/bugs <https://github.com/bachya/pyopenuv/issues>`_
   or `initiate a discussion on one <https://github.com/bachya/pyopenuv/issues/new>`_.
#. `Fork the repository <https://github.com/bachya/pyopenuv/fork>`_.
#. Install the dev environment: :code:`make init`.
#. Enter the virtual environment: :code:`pipenv shell`
#. Code your new feature or bug fix.
#. Write a test that covers your new functionality.
#. Run tests: :code:`make test`
#. Add yourself to AUTHORS.rst.
#. Submit a pull request!
