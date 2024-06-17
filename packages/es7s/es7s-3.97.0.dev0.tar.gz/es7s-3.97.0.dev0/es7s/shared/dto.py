# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t
from collections import OrderedDict
from collections.abc import Iterable
from dataclasses import dataclass, field
from math import inf

from .ipc import IDTO

_T = t.TypeVar("_T")


@dataclass
class ValueRange:
    min: float = inf
    max: float = -inf

    def apply(self, *vals: float):
        for val in vals:
            self.min = min(self.min, val)
            self.max = max(self.max, val)


@dataclass(unsafe_hash=True)
class BatteryInfo:
    MAX_LEVEL = 100

    level: int | float = None
    is_charging: bool = None
    remaining_sec: int = None

    def __post_init__(self):
        self.level = max(0, min(self.MAX_LEVEL, self.level))

    @property
    def is_max(self) -> bool:
        return self.level is not None and round(self.level) >= self.MAX_LEVEL


@dataclass
class DockerStatus:
    match_amount: int = 0
    container_names: list[str] = field(default_factory=list)
    updated_in_prev_tick: bool = False

    def __hash__(self) -> int:
        return hash(
            frozenset([self.match_amount, self.updated_in_prev_tick, *self.container_names])
        )


DockerInfo = dict[str, DockerStatus]


@dataclass(frozen=True)
class VoltageInfo:
    values_mv: OrderedDict[str, float]
    range_mv: ValueRange

    def __hash__(self) -> int:
        return hash(frozenset(self.values_mv))


@dataclass(frozen=True)
class WeatherInfo:
    location: str
    fields: list[str]

    def __hash__(self) -> int:
        return hash(frozenset([self.location, *self.fields]))


@dataclass(frozen=True)
class CpuInfo:
    freq_mhz: float = None
    load_perc: float = None
    load_avg: tuple[float, float, float] = None
    core_count: int = None
    thread_count: int = None


@dataclass(frozen=True)
class MemoryInfo:
    phys_used: int = None
    phys_total: int = None
    swap_used: int = None
    swap_total: int = None


@dataclass(frozen=True)
class TemperatureInfo:
    values_c: list[tuple[str, float]]
    range_c: ValueRange

    def __hash__(self) -> int:
        return hash(frozenset(self.values_c))


@dataclass(frozen=True)
class FanInfo:
    values_rpm: list[int]
    range_rpm: ValueRange

    def max(self) -> int:
        return max(self.values_rpm or [0])

    def __hash__(self) -> int:
        return hash(frozenset([*self.values_rpm]))


@dataclass(frozen=True)
class DiskUsageInfo:
    free: int
    total: int
    used_perc: float


@dataclass(frozen=True)
class DiskMountsInfo:
    mounts: dict[str, DiskUsageInfo]

    def __hash__(self) -> int:
        return hash(frozenset([*self.mounts.keys(), *self.mounts.values()]))


@dataclass(frozen=True)
class LoginInfo:
    user: str
    ip: str
    dt: str


@dataclass(frozen=True)
class LoginsInfo:
    parsed: list[LoginInfo]
    raw: list[str]

    def __hash__(self) -> int:
        return hash(frozenset([*self.parsed, *self.raw]))


@dataclass(frozen=True)
class DiskIoInfoStats:
    mbps: float = 0.0
    max_mbps: float = 0.0

    @property
    def ratio(self) -> float:
        if self.max_mbps == 0.0:
            return 0.0
        return self.mbps / self.max_mbps


@dataclass(frozen=True)
class DiskIoInfo:
    read: DiskIoInfoStats = DiskIoInfoStats()
    write: DiskIoInfoStats = DiskIoInfoStats()
    busy_ratio: float = None


DiskInfo = DiskUsageInfo | DiskIoInfo | DiskMountsInfo


@dataclass(frozen=True)
class NetworkCountryInfo(IDTO):
    ip: str = IDTO._map("query")
    country: str = IDTO._map("countryCode")
    continent: str = IDTO._map("continentCode")
    city: str = IDTO._map()
    isp: str = IDTO._map()
    mobile: bool = IDTO._map()
    proxy: bool = IDTO._map()
    hosting: bool = IDTO._map()


@dataclass(frozen=True)
class NetworkLatencyInfo:
    failed_ratio: float = None
    latency_s: float = None


@dataclass(frozen=True)
class NetworkUsageInfoStats:
    bps: float = None
    ratio: float = None
    drops: int = 0
    errors: int = 0


@dataclass(frozen=True)
class NetworkUsageInfo:
    interface: str = None
    isup: bool = None
    sent: NetworkUsageInfoStats = None
    recv: NetworkUsageInfoStats = None
    vpn: bool = None

    @property
    def stats(self) -> Iterable[NetworkUsageInfoStats]:
        yield self.sent
        yield self.recv


NetworkInfo = NetworkUsageInfo | NetworkLatencyInfo | NetworkCountryInfo


@dataclass(unsafe_hash=True)
class ShocksProxyInfo:
    name: str
    worker_up: bool = None
    running: bool = None
    healthy: bool = None
    latency_s: float = None
    proxy_latency_s: float = None


@dataclass(frozen=True)
class ShocksInfo:
    tunnel_amount: int = None
    running_amount: int = None
    healthy_amount: int = None
    proxies: frozenset[ShocksProxyInfo] = None
    relay_listeners_amount: int = None
    relay_connections_amount: int = None


@dataclass(frozen=True)
class SystemCtlInfo:
    status: str = None
    ok: bool = None


@dataclass(frozen=True)
class TimestampInfo:
    ts: int = None
    ok: bool = None
