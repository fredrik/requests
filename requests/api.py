# -*- coding: utf-8 -*-

"""
requests.api
~~~~~~~~~~~~

This module impliments the Requests API.

:copyright: (c) 2011 by Kenneth Reitz.
:license: ISC, see LICENSE for more details.

"""

from . import config
from .models import Request, Response, AuthObject
from .status_codes import codes
from .hooks import dispatch_hook
from .utils import cookiejar_from_dict, header_expand


__all__ = ('request', 'get', 'head', 'post', 'patch', 'put', 'delete')

def request(method, url,
    params=None, data=None, headers=None, cookies=None, files=None, auth=None,
    timeout=None, allow_redirects=False, proxies=None, hooks=None, return_response=True):

    """Constructs and sends a :class:`Request <Request>`.
    Returns :class:`Response <Response>` object.

    :param method: method for the new :class:`Request` object.
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
    :param data: (optional) Dictionary or bytes to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of 'filename': file-like-objects for multipart encoding upload.
    :param auth: (optional) AuthObject to enable Basic HTTP Auth.
    :param timeout: (optional) Float describing the timeout of the request.
    :param allow_redirects: (optional) Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param return_response: (optional) If False, an un-sent Request object will returned.
    """

    method = str(method).upper()

    if cookies is None:
        cookies = {}

    cookies = cookiejar_from_dict(cookies)

    # Expand header values
    if headers:
        for k, v in headers.items() or {}:
            headers[k] = header_expand(v)

    args = dict(
        method = method,
        url = url,
        data = data,
        params = params,
        headers = headers,
        cookiejar = cookies,
        files = files,
        auth = auth,
        hooks = hooks,
        timeout = timeout or config.settings.timeout,
        allow_redirects = allow_redirects,
        proxies = proxies or config.settings.proxies,
    )

    # Arguments manipulation hook.
    args = dispatch_hook('args', hooks, args)

    r = Request(**args)

    # Pre-request hook.
    r = dispatch_hook('pre_request', hooks, r)

    # Don't send if asked nicely.
    if not return_response:
        return r

    # Send the HTTP Request.
    r.send()

    # Post-request hook.
    r = dispatch_hook('post_request', hooks, r)

    # Response manipulation hook.
    r.response = dispatch_hook('response', hooks, r.response)

    return r.response


def get(url, **kwargs):

    """Sends a GET request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param **kwargs: Optional arguments that ``request`` takes.
    """


    kwargs.setdefault('allow_redirects', True)
    return request('GET', url, **kwargs)


def head(url, **kwargs):
    """Sends a HEAD request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param **kwargs: Optional arguments that ``request`` takes.
    """

    kwargs.setdefault('allow_redirects', True)
    return request('HEAD', url, **kwargs)


def post(url, data='', **kwargs):
    """Sends a POST request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary or bytes to send in the body of the :class:`Request`.
    :param **kwargs: Optional arguments that ``request`` takes.
    """

    return request('post', url, data=data, **kwargs)


def put(url, data='', **kwargs):
    """Sends a PUT request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary or bytes to send in the body of the :class:`Request`.
    :param **kwargs: Optional arguments that ``request`` takes.
    """

    return request('put', url, data=data, **kwargs)


def patch(url, data='', **kwargs):
    """Sends a PATCH request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary or bytes to send in the body of the :class:`Request`.
    :param **kwargs: Optional arguments that ``request`` takes.
    """

    return request('patch', url, **kwargs)


def delete(url, **kwargs):
    """Sends a DELETE request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param **kwargs: Optional arguments that ``request`` takes.
    """

    return request('delete', url, **kwargs)
