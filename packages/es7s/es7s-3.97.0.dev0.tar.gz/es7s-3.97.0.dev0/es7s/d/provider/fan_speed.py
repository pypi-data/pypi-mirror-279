# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import psutil

from es7s.shared import FanInfo, ValueRange, SocketTopic
from ._base import DataProvider


class FanSpeedProvider(DataProvider[FanInfo]):
    def __init__(self):
        self._range_rpm = ValueRange()
        super().__init__("fan", SocketTopic.FAN)

    def _collect(self) -> FanInfo:
        vals = psutil.sensors_fans().values()
        vals_cur = [val.current for sens in vals for val in sens]
        vals_flt = [*filter(lambda v: v < 64000, vals_cur)]
        # ^ filter parasite values ≈65500, 8-bit "-1" maybe
        self._range_rpm.apply(*vals_flt)
        return FanInfo(vals_flt, self._range_rpm)
