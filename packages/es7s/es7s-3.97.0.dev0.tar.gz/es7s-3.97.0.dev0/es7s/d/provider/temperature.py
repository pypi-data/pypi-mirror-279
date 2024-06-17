# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import psutil

from es7s.shared import TemperatureInfo, ValueRange, SocketTopic
from ._base import DataProvider


class TemperatureProvider(DataProvider[TemperatureInfo]):
    def __init__(self):
        self._range_c = ValueRange()
        super().__init__("temperature", SocketTopic.TEMPERATURE)

    def _collect(self) -> TemperatureInfo:
        values = list()
        for k, v in psutil.sensors_temperatures().items():
            for shwt in v:
                if not shwt.current:
                    continue
                result_key = k + ("/" + shwt.label if shwt.label else "")
                values.append((result_key, shwt.current))
                self._range_c.apply(shwt.current)

        return TemperatureInfo(values_c=values, range_c=self._range_c)
