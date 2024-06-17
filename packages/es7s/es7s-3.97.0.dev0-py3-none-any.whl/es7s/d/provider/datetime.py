# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from ._base import DataProvider
from ...shared import SocketTopic


class DatetimeProvider(DataProvider[None]):
    def __init__(self):
        super().__init__('datetime', SocketTopic.DATETIME)

    def _collect(self) -> None:
        return   # will be taken from socket message timestamp
