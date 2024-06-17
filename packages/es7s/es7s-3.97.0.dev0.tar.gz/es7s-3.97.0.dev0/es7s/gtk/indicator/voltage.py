# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from es7s_commons import median

from es7s.shared import SocketMessage, VoltageInfo, SocketTopic
from ._base import _BaseIndicator
from ._icon_selector import NoopIconSelector


class IndicatorVoltage(_BaseIndicator[VoltageInfo, NoopIconSelector]):
    def __init__(self):
        self.config_section = "indicator.voltage"

        super().__init__(
            indicator_name="voltage",
            socket_topic=SocketTopic.VOLTAGE,
            icon_selector=NoopIconSelector(),
            title="Voltage",
            pseudo_hide=True,
        )
        self._hidden.value = True
        self._update_visibility()

    def _render(self, msg: SocketMessage[VoltageInfo]):
        value_str = "{:.1f}V".format(median(sorted(msg.data.values_mv.values())) / 1e3)
        self._update_title(f"{self._title_base}\t\t{value_str}", for_mgr=True)
