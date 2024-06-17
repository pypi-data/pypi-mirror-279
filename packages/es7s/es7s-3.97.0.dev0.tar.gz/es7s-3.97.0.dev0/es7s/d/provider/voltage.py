# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import glob
import os
from collections import OrderedDict

from es7s.shared import VoltageInfo, ValueRange, SocketTopic
from ._base import DataProvider


class VoltageProvider(DataProvider[VoltageInfo]):
    def __init__(self):
        self._extractor = _Extractor()
        super().__init__("voltage", SocketTopic.VOLTAGE, 2.0)

    def _collect(self) -> VoltageInfo:
        return self._extractor.extract()


class _Extractor:
    _PATH_GLOB = "/sys/class/hwmon/hwmon*/"
    _SUBPATH_GLOBS = ["in*", "curr*"]

    def __init__(self):
        self._range_mv = ValueRange()

    def extract(self) -> VoltageInfo:
        values_mv: OrderedDict[str, float] = OrderedDict()

        for subglob in self._SUBPATH_GLOBS:
            for path in glob.glob(self._PATH_GLOB + subglob):
                if not os.path.isfile(path):
                    continue
                with open(path, "rt") as file:
                    try:
                        if value := float(file.readlines(1)[0].strip()):
                            values_mv[path] = value
                            self._range_mv.apply(value)
                    except (IndexError, ValueError):
                        continue

        if len(values_mv):
            return VoltageInfo(values_mv, self._range_mv)
        raise RuntimeError("No voltage info found")
