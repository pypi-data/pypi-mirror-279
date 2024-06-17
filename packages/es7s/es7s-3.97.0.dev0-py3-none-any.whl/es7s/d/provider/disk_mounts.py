# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re

import psutil

from es7s.shared import DiskMountsInfo, DiskUsageInfo
from es7s.shared import get_merged_uconfig, SocketTopic
from ._base import DataProvider


class DiskMountsProvider(DataProvider[DiskMountsInfo]):
    def __init__(self):
        super().__init__("disk-mounts", SocketTopic.DISK_MOUNTS, poll_interval_sec=5)

    def _collect(self) -> DiskMountsInfo:
        ucs = get_merged_uconfig().get_section("provider." + self._config_var)
        mp_filter = ucs.get("mountpoint-filter-regex", fallback=r"^")

        result = dict()
        for dp in psutil.disk_partitions(all=True):
            if re.match(mp_filter, dp.mountpoint):
                du = psutil.disk_usage(dp.mountpoint)
                dui = DiskUsageInfo(free=du.free, total=du.total, used_perc=du.percent)
                result.update({dp.mountpoint: dui})
        return DiskMountsInfo(result)
