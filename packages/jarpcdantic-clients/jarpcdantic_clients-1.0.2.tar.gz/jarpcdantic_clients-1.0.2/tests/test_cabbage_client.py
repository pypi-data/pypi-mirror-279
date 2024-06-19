# -*- coding: utf-8 -*-
import json

import jarpc
import pytest
from cabbage import AmqpConnection
from cabbage.test_utils import FakeAsyncAmqpRpc

from jarpcdantic_clients import CabbageTransport, create_cabbage_client


class TestCabbageClient:

    def test_factory(self):
        amqp_rpc = FakeAsyncAmqpRpc(connection=AmqpConnection())
        client = create_cabbage_client(amqp_rpc=amqp_rpc, exchange="test_exchange")
        assert isinstance(client, jarpcdantic.AsyncJarpcClient)
        assert isinstance(client._transport, CabbageTransport)

    @pytest.mark.asyncio
    async def test_call(self):
        amqp_rpc = FakeAsyncAmqpRpc(connection=AmqpConnection())
        client = create_cabbage_client(amqp_rpc=amqp_rpc, exchange="test_exchange")

        method = "method_name"
        expected_result = "some_result"
        response = json.dumps(
            {"result": expected_result, "request_id": "some_id", "id": "some_id"}
        )
        amqp_rpc.set_response(routing_key=method, data=response)

        result = await client(method=method, params={})
        assert result == expected_result
