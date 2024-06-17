# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from collections.abc import Iterable
from functools import lru_cache

import pytermor as pt
from pytermor import format_auto_float, formatter_bytes_human, StaticFormatter

from es7s.shared import DiskUsageInfo, DiskInfo, DiskIoInfo, uconfig, DiskMountsInfo
from es7s.shared import SocketMessage, SocketTopic
from ._base import _BaseIndicator, IValue
from ._icon_selector import ThresholdIconSelector, IconEnum, ThresholdMap
from ._state import _BoolState, CheckMenuItemConfig, RadioMenuItemConfig


class DiskIconEnum(IconEnum):
    WAIT = "wait.svg"


class DiskIconPartBusyEnum(IconEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAX = "max"


class DiskIconSelector(ThresholdIconSelector):
    @lru_cache
    def get_icon_names_set(self) -> set[str]:
        return {*DiskIconEnum, *super().get_icon_names_set()}


class ValueUsed(IValue):
    def __init__(self):
        super().__init__()
        self._value_perc: float | None = None
        self._warn_ratio: float | None = uconfig.get_for(self).get("used-warn-level-ratio", float)
        self.state = _BoolState(
            config_var=("indicator.disk", "label-used"),
            gconfig=CheckMenuItemConfig("Show used space (%)", sep_before=True),
        )

    def set(self, dto: DiskUsageInfo):
        self._value_perc = dto.used_perc
        super().set()

    @property
    def warn_level_exceeded(self) -> bool:
        if self.value_ratio is None:
            return False
        return self.value_ratio >= self._warn_ratio

    @property
    def value_perc(self) -> float | None:
        return self._value_perc

    @property
    def value_ratio(self) -> float | None:
        if self._value_perc is not None:
            return self._value_perc / 100

    def _format(self) -> str | None:
        return f"{100 * self.value_ratio:2.0f}%"

    def format_label(self) -> str | None:
        if self._value_perc is not None and (self.state or self.attention):
            return self._format()

    def format_details(self) -> str | None:
        if self._value_perc is not None:
            return self._format() + " used"


class ValueFree(IValue):
    def __init__(self):
        super().__init__()
        self._value_bytes: int | None = None
        self._value_bytes_total: int | None = None
        self.state = _BoolState(
            config_var=("indicator.disk", "label-free"),
            gconfig=CheckMenuItemConfig("Show free space (GB/TB)"),
        )

    def set(self, dto: DiskUsageInfo):
        self._value_bytes = dto.free
        self._value_bytes_total = dto.total
        super().set()

    def _format(self, v: int) -> str:
        v_gb = v / 1000**3
        v_tb = v / 1000**4
        if v_gb < 1:
            return "< 1G"
        if v_gb < 1000:
            return format_auto_float(v_gb, 3, False) + "G"
        return format_auto_float(v_tb, 3, False) + "T"

    def format_label(self) -> str | None:
        if self._value_bytes is not None and self.state:
            return self._format(self._value_bytes)

    def format_details(self) -> str | None:
        if self._value_bytes is not None:
            result = self._format(self._value_bytes) + "%s free"
            if self._value_bytes_total is not None:
                result %= "/" + self._format(self._value_bytes_total)
            return result


class ValueMounts(IValue):
    def __init__(self):
        super().__init__()
        self._value: int | None = None
        self._prev_value: int | None = None
        self.state = _BoolState(
            config_var=("indicator.disk", "label-mounts"),
            gconfig=CheckMenuItemConfig("Show mounts amount", sep_before=True),
        )

    def set(self, dto: DiskMountsInfo):
        self._prev_value = self._value
        self._value = len(dto.mounts)
        super().set()

    @property
    def warn_level_exceeded(self) -> bool:
        if self._value is None:
            return False
        return self._value != self._prev_value

    def format_label(self) -> str | None:
        if self._value is not None and (self.state or self.attention):
            return f"({self._value:d})"

    def format_details(self) -> None:
        return None


class ValueBusy(IValue):
    def __init__(self):
        super().__init__()
        self._value_ratio: float | None = None
        self._warn_ratio: float | None = uconfig.get_for(self).get("busy-warn-level-ratio", float)
        self.state = _BoolState(
            config_var=("indicator.disk", "label-busy"),
            gconfig=CheckMenuItemConfig("Show busy ratio (%)", sep_before=True),
        )

    def set(self, dto: DiskIoInfo):
        self._value_ratio = dto.busy_ratio
        super().set()

    @property
    def warn_level_exceeded(self) -> bool:
        if self._value_ratio is None:
            return False
        return self._value_ratio >= self._warn_ratio

    @property
    def value_perc(self) -> float | None:
        if self._value_ratio is not None:
            return 100 * self._value_ratio

    def format_label(self) -> str | None:
        if self._value_ratio is not None and (self.state or self.attention):
            return f"{self.value_perc:3.0f}%"

    def format_details(self) -> str:
        busy_str = "---"
        if self._value_ratio is not None:
            busy_str = f"{self.value_perc:3.0f}%"
        return f"{busy_str} busy"


class ValueIoSpeed(IValue):
    formatter: StaticFormatter = StaticFormatter(
        formatter_bytes_human,
        max_value_len=4,
        discrete_input=False,
        prefix_refpoint_shift=2,
    )

    def __init__(self):
        super().__init__()
        self._value_read_mbps: float | None = None
        self._value_write_mbps: float | None = None

        self._state_off = _BoolState(
            config_var=("indicator.disk", "label-io"),
            config_var_value="off",
            gconfig=RadioMenuItemConfig("No IO speed", sep_before=True, group="indicator.disk"),
        )
        self._state_read = _BoolState(
            config_var=("indicator.disk", "label-io"),
            config_var_value="read",
            gconfig=RadioMenuItemConfig("Show read speed (bytes/s)", group="indicator.disk"),
        )
        self._state_write = _BoolState(
            config_var=("indicator.disk", "label-io"),
            config_var_value="write",
            gconfig=RadioMenuItemConfig("Show write speed (bytes/s)", group="indicator.disk"),
        )
        self._state_both = _BoolState(
            config_var=("indicator.disk", "label-io"),
            config_var_value="both",
            gconfig=RadioMenuItemConfig("Show both speeds (bytes/s)", group="indicator.disk"),
        )
        self._state_total = _BoolState(
            config_var=("indicator.disk", "label-io"),
            config_var_value="total",
            gconfig=RadioMenuItemConfig("Show total speed (sum, bytes/s)", group="indicator.disk"),
        )
        self.states = [
            self._state_off,
            self._state_read,
            self._state_write,
            self._state_both,
            self._state_total,
        ]

    def set(self, dto: DiskIoInfo):
        self._value_read_mbps = dto.read.mbps
        self._value_write_mbps = dto.write.mbps
        super().set()

    def _format(self, type: str, mbps: float) -> str:
        return f"{type}{self.formatter.format(mbps)}"

    def format_label(self) -> Iterable[str]:
        if self._state_total:
            if self._value_read_mbps is not None and self._value_write_mbps is not None:
                yield self._format("", self._value_read_mbps + self._value_write_mbps)
        else:
            if self._value_read_mbps is not None and (self._state_read or self._state_both):
                yield self._format("↑", self._value_read_mbps)
            if self._value_write_mbps is not None and (self._state_write or self._state_both):
                yield self._format("↓", self._value_write_mbps)

    def format_details(self) -> str:
        return (
            self._format("R↑", self._value_read_mbps or 0)
            + " / "
            + self._format("W↓", self._value_write_mbps or 0)
        )


class IndicatorDisk(_BaseIndicator[DiskInfo, DiskIconSelector]):
    def __init__(self):
        self.config_section = "indicator.disk"

        self._value_used = ValueUsed()
        self._value_free = ValueFree()
        self._value_busy = ValueBusy()
        self._value_io = ValueIoSpeed()
        self._value_mounts = ValueMounts()

        super().__init__(
            indicator_name="disk",
            socket_topic=[SocketTopic.DISK_USAGE, SocketTopic.DISK_IO, SocketTopic.DISK_MOUNTS],
            icon_selector=DiskIconSelector(
                ThresholdMap(
                    **{
                        DiskIconPartBusyEnum.MAX.value: 95,
                        DiskIconPartBusyEnum.HIGH.value: 75,
                        DiskIconPartBusyEnum.MEDIUM.value: 25,
                        DiskIconPartBusyEnum.LOW.value: 0,
                    },
                ),
                ThresholdMap(100, 99, 98, 95, 92, *range(90, -10, -10)),
                subpath="disk",
                path_dynamic_tpl="%s-%s.svg",
                name_default=DiskIconEnum.WAIT,
            ),
            title="Storage",
            states=[
                self._value_used.state,
                self._value_free.state,
                self._value_busy.state,
                *self._value_io.states,
                self._value_mounts.state,
            ],
        )

    #
    def _render(self, msg: SocketMessage[DiskInfo]):
        usage_dto = self._get_last_dto(DiskUsageInfo, msg.data)
        io_dto = self._get_last_dto(DiskIoInfo, msg.data)
        mounts_dto = self._get_last_dto(DiskMountsInfo, msg.data)

        details_root = "(0) /\t"
        details_mounts = []

        if usage_dto:
            self._value_free.set(usage_dto)
            self._value_used.set(usage_dto)
            details_root += " ⋅ ".join(
                pt.filtern(
                    [
                        self._value_used.format_details(),
                        self._value_free.format_details(),
                    ]
                )
            )

        if io_dto:
            self._value_busy.set(io_dto)
            self._value_io.set(io_dto)
            details_root += "\n\t" + " ⋅ ".join(
                [
                    self._value_busy.format_details(),
                    self._value_io.format_details(),
                ]
            )

        if mounts_dto:
            self._value_mounts.set(mounts_dto)
            for (idx, (k, v)) in enumerate(mounts_dto.mounts.items()):
                details_mounts.append(f"({idx+1}) {k}\t{v.used_perc:3.1f}%")

        self._update_title_attention(
            self._value_busy.warn_level_exceeded or self._value_used.warn_level_exceeded
        )
        self._update_details("\n".join([details_root] + details_mounts))
        self._render_result(
            self._format_result(),
            icon=self._icon_selector.select(
                self._value_busy.value_perc, self._value_used.value_perc
            ),
        )

    def _format_result(self) -> str:
        parts = pt.filtern(
            [
                self._value_used.format_label(),
                self._value_free.format_label(),
                self._value_busy.format_label(),
                *self._value_io.format_label(),
                self._value_mounts.format_label(),
            ]
        )
        return " ".join(parts).rstrip()
