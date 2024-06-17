# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re
import time

from es7s.shared import SocketTopic
from es7s.shared import TimestampInfo
from ._base import DataProvider


class TimestampProvider(DataProvider[TimestampInfo]):
    def __init__(self):
        super().__init__("timestamp", SocketTopic.TIMESTAMP, 23.0)
        self._last_ts: int | None = None

    def _collect(self) -> TimestampInfo:
        url = self.uconfig().get("url")
        try:
            self._network_req_event.set()
            time.sleep(0.25)

            response = self._make_request(url)
            data = response.text
            data_match = re.match(r"(\d{10})", data.strip())
            if not data_match:
                raise ValueError(f"Unexpected response: '{data}'")
            self._last_ts = int(data_match.group(1))

        finally:
            self._network_req_event.clear()

        return TimestampInfo(ts=self._last_ts, ok=True)

    def _reset(self) -> TimestampInfo:
        return TimestampInfo(ts=self._last_ts, ok=False)
