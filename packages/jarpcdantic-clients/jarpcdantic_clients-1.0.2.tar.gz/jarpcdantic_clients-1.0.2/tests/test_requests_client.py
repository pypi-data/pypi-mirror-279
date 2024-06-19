# -*- coding: utf-8 -*-
import json
from unittest import mock

import jarpc
import pytest
import requests

from jarpcdantic_clients import RequestsTransport, create_requests_client


class TestRequestsClient:

    def test_factory(self):
        client = create_requests_client(url="http://test/")
        assert isinstance(client, jarpcdantic.JarpcClient)
        assert isinstance(client._transport, RequestsTransport)
        client._transport.close_session()

    def test_call(self):
        expected_result = "some_result"
        response = json.dumps(
            {"result": expected_result, "request_id": "some_id", "id": "some_id"}
        )

        with mock.patch(
            "jarpc_clients.requests_client.requests.Session"
        ) as SessionMock:
            session_instance = SessionMock.return_value
            response_object = session_instance.request.return_value
            response_object.text = response

            client = create_requests_client(url="http://test/")
            result = client(method="method_name", params={})

        assert result == expected_result

    def test_timeout_error(self):
        with pytest.raises(jarpcdantic.JarpcTimeout):
            with mock.patch(
                "jarpc_clients.requests_client.requests.Session"
            ) as SessionMock:
                session_instance = SessionMock.return_value
                session_instance.request = mock.Mock(side_effect=requests.Timeout())

                client = create_requests_client(url="http://test/")
                client(method="method_name", params={}, ttl=0)
