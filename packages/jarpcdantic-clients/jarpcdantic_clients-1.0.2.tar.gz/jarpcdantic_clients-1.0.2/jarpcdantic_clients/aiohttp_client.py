# -*- coding: utf-8 -*-
from typing import Any, Callable, Optional

import jarpcdantic

try:
    import aiohttp
except ImportError:
    aiohttp = None


class AiohttpTransport:
    """
    Transport to make rpc as HTTP request using aiohttp library.

    To use this transport you need to install "aiohttp" package.
    """

    default_headers = {"Content-Type": "application/json"}

    def __init__(self, url: str, session=None, request_kwargs: Optional[dict] = None):
        """
        Init transport.
        You can pass any aiohttp request kwarg such as `ssl`, `timeout`, `headers`, `params` etc.

        If JARPC request ttl is specified, it will be used as timeout.
        To define default request timeout pass `timeout` kwarg.

        :param url: RPC server URL
        :param session: optional `aiohttp.ClientSession` object
        :param request_kwargs: `aiohttp.ClientSession.request` kwargs
        """
        self.session = session

        request_kwargs = request_kwargs or {}
        request_kwargs["headers"] = {
            **self.default_headers,
            **request_kwargs.get("headers", {}),
        }
        self.request_kwargs = {"method": "POST", "url": url, **request_kwargs}

    async def __call__(
        self,
        request_string: str,
        request: jarpcdantic.JarpcRequest,
        session=None,
        request_kwargs: Optional[dict] = None,
    ) -> str:
        """
        Call method.
        You can pass any aiohttp request kwarg such as `ssl`, `timeout`, `headers`, `params` etc.

        If JARPC request is specified, it will be used as timeout.
        To define default request timeout pass `timeout` kwarg.

        :param request_string: serialized JARPC request
        :param request: JARPC request object
        :param session: optional `aiohttp.ClientSession` object
        :param request_kwargs: `aiohttp.ClientSession.request` kwargs
        :return: RPC result
        """
        if isinstance(request_string, str):
            request_string = request_string.encode("utf-8")

        request_kwargs = {
            **self.request_kwargs,
            "data": request_string,
            **(request_kwargs or {}),
        }
        if request.ttl is not None:
            request_kwargs["timeout"] = request.ttl

        if session is None:
            session = await self.get_session()

        try:
            async with session.request(**request_kwargs) as http_request:
                return await http_request.text()
        except aiohttp.ServerTimeoutError:
            raise jarpcdantic.JarpcTimeout()

    async def get_session(self):
        """
        Get or create `aiohttp.ClientSession` object.
        This method is asynchronous because `aiohttp.ClientSession` should be created from async function.
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close_session(self, *args, **kwargs):
        """
        Close connections and release resources.
        Accept any args and kwargs to be compatible with different interfaces.
        """
        await self.session.close()


def create_aiohttp_client(
    url: str,
    session=None,
    request_kwargs: Optional[dict] = None,
    default_ttl: Optional[float] = None,
    default_rpc_ttl: Optional[float] = None,
    default_notification_ttl: Optional[float] = None,
    loads: Callable[[str], Any] = jarpcdantic.format.json_loads,
    dumps: Callable[[Any], str] = jarpcdantic.format.json_dumps,
) -> jarpcdantic.AsyncJarpcClient:
    """
    Create JARPC client with aiohttp transport.

    :param url: RPC server URL
    :param session: optional `aiohttp.ClientSession` object
    :param request_kwargs: `aiohttp.ClientSession.request` kwargs
    :param default_ttl: float time interval while calling still actual
    :param default_rpc_ttl: default_ttl for rsvp=True calls (if None default_ttl will be used)
    :param default_notification_ttl: default_ttl for rsvp=False calls (if None default_ttl will be used)
    :param loads: json loads
    :param dumps: json dumps
    :return: AsyncJarpcClient object
    """
    transport = AiohttpTransport(
        url=url, session=session, request_kwargs=request_kwargs
    )
    return jarpcdantic.AsyncJarpcClient(
        transport=transport,
        default_ttl=default_ttl,
        default_rpc_ttl=default_rpc_ttl,
        default_notification_ttl=default_notification_ttl,
        loads=loads,
        dumps=dumps,
    )
