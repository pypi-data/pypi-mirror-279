# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import threading as th
import typing as t
from logging import getLogger

import pytermor as pt

from .exception import DataCollectionError
from .log import TRACE
from .threads import ThreadSafeCounter


class Requester:
    DEFAULT_TIMEOUT = 10
    HTTP_RESPONSE_FILTERS = [
        pt.StringLinearizer(),
    ]

    network_request_id = ThreadSafeCounter()

    def __init__(self, network_req_event: th.Event = None):
        self._network_req_event: th.Event = network_req_event or th.Event()

    def make_request(
        self,
        url: str,
        timeout: float = DEFAULT_TIMEOUT,
        request_fn: t.Callable[[str], "Response"] = None,
        log_response_body: bool = True,
        **kwargs,
    ) -> "Response":
        import requests

        try:
            request_id = self.network_request_id.next()
            self._network_req_event.set()
            self._log_http_request(request_id, url)
            if not request_fn:
                request_fn = lambda _url: requests.get(_url, timeout=timeout, **kwargs)
            response = request_fn(url)
            self._log_http_response(request_id, response, with_body=log_response_body)

        except requests.exceptions.ConnectionError as e:
            getLogger(__package__).error(e)
            raise DataCollectionError()

        except requests.RequestException as e:
            getLogger(__package__).exception(e)
            raise DataCollectionError()

        finally:
            self._network_req_event.clear()

        if not response.ok:
            getLogger(__package__).warning(f"Request failed: HTTP {response.status_code}")
            [getLogger(__package__).debug(h) for h in response.headers]
            raise DataCollectionError(http_code=response.status_code)
        return response

    def _log_http_request(self, req_id: int | str, url: str, method: str = "GET"):
        getLogger(__package__).info(f"[#{req_id}] > {method} {url}")

    def _log_http_response(self, req_id: int | str, response: "Response", with_body: bool):
        msg_resp = f"[#{req_id}] < HTTP {response.status_code}"
        msg_resp += ", " + pt.format_si(response.elapsed.total_seconds(), "s")
        msg_resp += ", " + pt.format_si_binary(len(response.text)) + " body"
        msg_resp += ", " + str(len(response.request.headers)) + " request headers"
        msg_resp += ", " + str(len(response.headers)) + " response headers"
        getLogger(__package__).info(msg_resp)

        getLogger(__package__).debug(
            f"[#{req_id}] > ["
            + ",".join(repr(f"{k}: {v}") for k, v in response.request.headers.items())
            + "]"
        )
        getLogger(__package__).debug(
            f"[#{req_id}] < ["
            + ",".join(repr(f"{k}: {v}") for k, v in response.headers.items())
            + "]"
        )

        if with_body:
            getLogger(__package__).log(
                TRACE,
                f'[#{req_id}] << "'
                + pt.apply_filters(response.text, *self.HTTP_RESPONSE_FILTERS)
                + '"',
            )
