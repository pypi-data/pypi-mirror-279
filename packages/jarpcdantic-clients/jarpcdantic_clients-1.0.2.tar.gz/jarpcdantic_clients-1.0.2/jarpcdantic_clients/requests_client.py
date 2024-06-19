# -*- coding: utf-8 -*-
from typing import Any, Callable, Optional

import jarpcdantic

try:
    import requests
except ImportError:
    requests = None


class RequestsTransport:
    """
    Transport to make rpc as HTTP request using requests library.

    To use this transport you need to install "requests" package.
    """

    default_headers = {"Content-Type": "application/json"}

    def __init__(self, url: str, session=None, request_kwargs: Optional[dict] = None):
        """
        Init transport.
        You can pass any request kwarg such as `verify`, `timeout`, `headers`, `params` etc.

        If JARPC request ttl is specified, it will be used as timeout.
        To define default request timeout pass `timeout` kwarg.

        :param url: RPC server URL
        :param session: optional `requests.Session` object
        :param request_kwargs: `requests.Session.request` kwargs
        """
        self.session = session or requests.Session()

        request_kwargs = request_kwargs or {}
        request_kwargs["headers"] = {
            **self.default_headers,
            **request_kwargs.get("headers", {}),
        }
        self.request_kwargs = {"method": "POST", "url": url, **request_kwargs}

    def __call__(
        self,
        request_string: str,
        request: jarpcdantic.JarpcRequest,
        session=None,
        request_kwargs: Optional[dict] = None,
    ) -> str:
        """
        Call method.
        You can pass any request kwarg such as `verify`, `timeout`, `headers`, `params` etc.

        If JARPC request ttl is specified, it will be used as timeout.
        To define default request timeout pass `timeout` kwarg.

        :param request_string: serialized JARPC request
        :param request: JARPC request object
        :param session: optional `requests.Session` object
        :param request_kwargs: `requests.Session.request` kwargs
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
            session = self.session

        try:
            return session.request(**request_kwargs).text
        except requests.Timeout:
            raise jarpcdantic.JarpcTimeout()

    def close_session(self, *args, **kwargs):
        """
        Close connections and release resources.
        Accept any args and kwargs to be compatible with different interfaces.
        """
        self.session.close()


def create_requests_client(
    url: str,
    session=None,
    request_kwargs: Optional[dict] = None,
    default_ttl: Optional[float] = None,
    default_rpc_ttl: Optional[float] = None,
    default_notification_ttl: Optional[float] = None,
    loads: Callable[[str], Any] = jarpcdantic.format.json_loads,
    dumps: Callable[[Any], str] = jarpcdantic.format.json_dumps,
) -> jarpcdantic.JarpcClient:
    """
    Create JARPC client with requests transport.

    :param url: RPC server URL
    :param session: optional `requests.Session` object
    :param request_kwargs: `requests.Session.request` kwargs
    :param default_ttl: float time interval while calling still actual
    :param default_rpc_ttl: default_ttl for rsvp=True calls (if None default_ttl will be used)
    :param default_notification_ttl: default_ttl for rsvp=False calls (if None default_ttl will be used)
    :param loads: json loads
    :param dumps: json dumps
    :return: JarpcClient object
    """
    transport = RequestsTransport(
        url=url, session=session, request_kwargs=request_kwargs
    )
    return jarpcdantic.JarpcClient(
        transport=transport,
        default_ttl=default_ttl,
        default_rpc_ttl=default_rpc_ttl,
        default_notification_ttl=default_notification_ttl,
        loads=loads,
        dumps=dumps,
    )
