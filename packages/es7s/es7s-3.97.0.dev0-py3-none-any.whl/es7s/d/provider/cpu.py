# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import psutil

from es7s.shared import CpuInfo, SocketTopic
from ._base import DataProvider


class CpuProvider(DataProvider[CpuInfo]):
    def __init__(self):
        super().__init__("cpu", SocketTopic.CPU)

    def _collect(self) -> CpuInfo:
        return CpuInfo(
            freq_mhz=psutil.cpu_freq().current,
            load_perc=psutil.cpu_percent(),
            load_avg=psutil.getloadavg(),
            core_count=psutil.cpu_count(False),
            thread_count=psutil.cpu_count(True),
        )
