# -*- coding: utf-8 -*-
import json

import aiohttp
import jarpc
import pytest
from aioresponses import aioresponses

from jarpcdantic_clients import AiohttpTransport, create_aiohttp_client


class TestAiohttpClient:

    def test_factory(self):
        client = create_aiohttp_client(url="http://test/")
        assert isinstance(client, jarpcdantic.AsyncJarpcClient)
        assert isinstance(client._transport, AiohttpTransport)

    @pytest.mark.asyncio
    async def test_call(self):
        test_url = "http://test/"
        client = create_aiohttp_client(url=test_url)

        expected_result = "some_result"
        response = json.dumps(
            {"result": expected_result, "request_id": "some_id", "id": "some_id"}
        )

        with aioresponses() as aiohttp_mock:
            aiohttp_mock.post(test_url, body=response)
            result = await client(method="method_name", params={})

        assert result == expected_result

        assert not client._transport.session.closed
        await client._transport.close_session()
        assert client._transport.session.closed

    @pytest.mark.asyncio
    async def test_timeout_error(self):
        test_url = "http://test/"
        client = create_aiohttp_client(url=test_url)

        with pytest.raises(jarpcdantic.JarpcTimeout):
            with aioresponses() as aiohttp_mock:
                aiohttp_mock.post(test_url, exception=aiohttp.ServerTimeoutError())
                await client(method="method_name", params={}, ttl=0)

        await client._transport.close_session()
