# -*- coding: utf-8 -*-
from typing import Optional

import jarpcdantic

try:
    import cabbagok
except ImportError:
    cabbage = None


class CabbageTransport:
    """
    Transport to make rpc through RabbitMQ using "cabbage" library.
    """

    def __init__(self, amqp_rpc, exchange: str, default_timeout: float = 60.0):
        """
        Init transport.
        :param amqp_rpc: cabbage AsyncAmqpRpc-object that should be connected before calling this transport
        :param exchange: RabbitMQ exchange
        :param default_timeout: default rpc timeout, used if JARPC request ttl is not specified
        """
        self.amqp_rpc = amqp_rpc
        self.exchange = exchange
        self.default_timeout = default_timeout

    async def __call__(
        self,
        request_string: str,
        request: jarpcdantic.JarpcRequest,
        correlation_id: Optional[str] = None,
    ) -> Optional[str]:
        """
        Call method assuming routing key is method name.

        :param request_string: serialized JARPCdantic request
        :param request: JARPCdantic request object
        :param correlation_id: optional transport kwarg
        :return: RPC result
        """
        return await self.amqp_rpc.send_rpc(
            exchange=self.exchange,
            destination=request.method,
            data=request_string,
            await_response=request.rsvp,
            timeout=self.default_timeout if request.ttl is None else request.ttl,
            correlation_id=correlation_id,
        )


def create_cabbage_client(
    amqp_rpc,
    exchange: str,
    default_timeout: Optional[float] = None,
    default_ttl: Optional[float] = None,
    default_rpc_ttl: Optional[float] = None,
    default_notification_ttl: Optional[float] = None,
) -> jarpcdantic.AsyncJarpcClient:
    """
    Create JARPC client with cabbage transport.

    :param amqp_rpc: cabbage AsyncAmqpRpc-object that should be connected before calling this transport
    :param exchange: RabbitMQ exchange
    :param default_timeout: default rpc timeout, used if JARPC request ttl is not specified
    :param default_ttl: float time interval while calling still actual
    :param default_rpc_ttl: default_ttl for rsvp=True calls (if None default_ttl will be used)
    :param default_notification_ttl: default_ttl for rsvp=False calls (if None default_ttl will be used)
    :return: AsyncJarpcClient object
    """
    transport = CabbageTransport(
        amqp_rpc=amqp_rpc, exchange=exchange, default_timeout=default_timeout
    )
    return jarpcdantic.AsyncJarpcClient(
        transport=transport,
        default_ttl=default_ttl,
        default_rpc_ttl=default_rpc_ttl,
        default_notification_ttl=default_notification_ttl,
    )
