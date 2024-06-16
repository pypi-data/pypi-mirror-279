"""This is a sample python file for testing functions from the source code."""

from __future__ import annotations

import unittest

from meteoswiss_async import MeteoSwissClient


class ClientTestCase(unittest.IsolatedAsyncioTestCase):

    async def test_hello(self):
        """
        This defines the expected usage, which can then be used in various test cases.
        Pytest will not execute this code directly, since the function does not contain the suffix "test"
        """
        client = await MeteoSwissClient.with_session()
        await client.close()
