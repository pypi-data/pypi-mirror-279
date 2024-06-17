from __future__ import annotations

import logging
import typing as t

log = logging.getLogger("red_utils.ext.httpx_utils")

from .constants import (
    default_headers,
)
from .validators import (
    validate_client,
    validate_headers,
    validate_method,
)

import httpx
from httpx import URL, BaseTransport, Client
from httpx._client import EventHook
from httpx._config import Limits
from httpx._types import (
    AsyncByteStream,
    AuthTypes,
    CertTypes,
    CookieTypes,
    HeaderTypes,
    ProxiesTypes,
    ProxyTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    SyncByteStream,
    TimeoutTypes,
    URLTypes,
    VerifyTypes,
)

def merge_headers(
    original_headers: dict[str, str] = default_headers,
    update_vals: dict[str, str] = None,
) -> dict[str, str]:
    """Merge header dicts into new headers dict."""
    validate_headers(original_headers)
    validate_headers(update_vals)

    try:
        _headers: dict = {**update_vals, **original_headers}

    except Exception as exc:
        msg = Exception(f"Unhandled exception merging header dicts. Details: {exc}")
        log.error(msg)

        raise exc

    return _headers


def update_headers(
    original_headers: dict[str, str] = default_headers,
    update_vals: dict[str, str] = None,
) -> dict[str, str]:
    validate_headers(original_headers)
    validate_headers(update_vals)

    try:
        ## Create a copy of original_headers to update
        new_headers: dict[str, str] = original_headers.copy()
        ## Update new_headers with update_vals dict
        new_headers.update(update_vals)

        return new_headers

    except Exception as exc:
        msg = Exception(f"Unhandled exception updating headers. Details: {exc}")
        log.error(msg)

        raise exc


def get_req_client(
    auth: AuthTypes | None = None,
    params: t.Union[QueryParamTypes, dict] | None = None,
    headers: t.Union[HeaderTypes, dict] | None = None,
    cookies: CookieTypes | None = None,
    verify: VerifyTypes = True,
    cert: CertTypes | None = None,
    http1: bool = True,
    http2: bool = False,
    proxy: ProxyTypes | None = None,
    proxies: ProxiesTypes | None = None,
    mounts: t.Mapping[str, BaseTransport | None] | None = None,
    timeout: t.Union[int, float, TimeoutTypes] | None = 5.0,
    follow_redirects: bool = False,
    limits: t.Union[dict, Limits] = {
        "max_connections": 100,
        "max_keepalive_connections": 20,
    },
    max_redirects: int | None = 20,
    event_hooks: t.Mapping[str, list[EventHook]] | None = None,
    base_url: URLTypes = "",
    transport: BaseTransport | None = None,
    app: t.Callable[..., t.Any] | None = None,
    trust_env: bool = True,
    default_encoding: str | bytes = "utf-8",
) -> httpx.Client:
    """Build an HTTPX Client from input parameters.

    Params:
        auth (AuthTypes | None):
        params (t.Union[QueryParamTypes, dict] | None):
        headers (t.Union[HeaderTypes, dict] | None):
        cookies (CookieTypes | None):
        verify (VerifyTypes):
        cert (CertTypes | None):
        http1 (bool):
        http2 (bool):
        proxy (ProxyTypes | None):
        proxies (ProxiesTypes | None):
        mounts (t.Mapping[str, BaseTransport | None] | None):
        timeout (t.Union[int, float, TimeoutTypes] | None):
        follow_redirects (bool):
        limits (t.Union[dict, Limits]):
        event_hooks (t.Mapping[str, list[EventHook]] | None):
        base_url (URLTypes):
        transport (BaseTransport | None):
        app (t.Callable[..., t.Any] | None):
        trust_env (bool):
        default_encoding (str | bytes):

    Returns:
        (httpx.Client): An initialized HTTPX client.

    """
    timeout: httpx.Timeout = httpx.Timeout(timeout)
    if isinstance(limits, dict):
        limits: Limits = Limits(**limits)

    try:
        _client: Client = Client(
            headers=headers,
            timeout=timeout,
            auth=auth,
            params=params,
            cookies=cookies,
            verify=verify,
            cert=cert,
            http1=http1,
            http2=http2,
            proxy=proxy,
            proxies=proxies,
            mounts=mounts,
            follow_redirects=follow_redirects,
            max_redirects=max_redirects,
            event_hooks=event_hooks,
            base_url=base_url,
            transport=transport,
            app=app,
            trust_env=trust_env,
            default_encoding=default_encoding,
        )
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception building HTTPX RequestClient. Details: {exc}"
        )
        log.error(msg)

        raise exc

    validate_client(_client)

    return _client


def build_request(
    method: str = "GET",
    url: t.Union[URL, str] = None,
    params: QueryParamTypes | None = None,
    headers: HeaderTypes | None = None,
    cookies: CookieTypes | None = None,
    content: RequestContent | None = None,
    data: RequestData | None = None,
    files: RequestFiles | None = None,
    json: t.Any | None = None,
    stream: t.Union[SyncByteStream, AsyncByteStream] | None = None,
    extensions: RequestExtensions | None = None,
) -> httpx.Request:
    """Build an `httpx.Request()` object from inputs.

    Params:
        method (str): (default="GET") The HTTP method for the request.
        url (str): The URL to send request to.
        files (list): List of files to send with request.
        data (Any): <UNDOCUMENTED>
        contents (bytes): Byte-encoded request content.
        params (dict): URL params for request. Pass each param as a key/value pair, like:
            `{"api_key": api_key, "days": 15, "page": 2}`
        headers (dict): Headers for request.
        cookies (dict): Cookies for request.
        extensions (dict): Extensions for request. Example: `{"timeout": {"connect": 5.0}}`.
        stream (httpx.SyncByteStream | httpx.AsyncByteSTream): <UNDOCUMENTED>
    """
    method: str = method.upper()
    method = validate_method(method=method)

    try:
        _request: httpx.Request = httpx.Request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            content=content,
            data=data,
            files=files,
            json=json,
            extensions=extensions,
            stream=stream,
        )
        return _request

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception building httpx.Request object. Details: {exc}"
        )
        log.error(msg)

        raise exc


def make_request(
    client: Client = None,
    url: str = None,
    method: str = "GET",
    headers: dict = None,
    timeout: int | None = None,
    data: dict | None = None,
) -> httpx.Response:
    """Make a request with HTTPX."""
    validate_method(method)

    if not client:
        log.warning(
            "No request client passed to make_request() function. Getting default client."
        )

        client = get_req_client(headers=headers, timeout=timeout, data=data)

    validate_client(client=client)

    if not isinstance(client, Client):
        raise TypeError(
            f"Invalid type for client: {type(client)}. Must be of type {type(Client)}"
        )

    if not url:
        raise ValueError("Missing request URL")

    if not isinstance(url, str):
        raise TypeError(f"Invalid type for request URL: {type(url)}")

    if timeout:
        if not isinstance(timeout, int):
            raise TypeError(f"Invalid type for timeout: {type(timeout)}")

    try:
        ## Determine type of request to make
        match method:
            case "GET":
                client = get_req_client(headers=headers, timeout=timeout)

                res = client.get(url=url)

            case _:
                raise ValueError(f"Invalid method: {method}")

        return res

    except Exception as exc:
        msg = Exception(f"Unhandled exception creating request client. Details: {exc}")
        log.error(msg)

        raise exc
