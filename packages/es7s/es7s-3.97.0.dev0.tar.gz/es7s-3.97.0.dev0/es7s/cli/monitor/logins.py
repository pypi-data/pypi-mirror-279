# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click
import pytermor as pt

from es7s.shared import SocketMessage, LoginsInfo, SocketTopic
from es7s.shared import Styles
from es7s.shared.styles import format_value_overflow
from ._base import CoreMonitor, MonitorCliCommand, CoreMonitorSettings, CoreMonitorConfig
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command

OUTPUT_WIDTH = 3


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="active OS-level user sessions",
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    LoginsMonitor(ctx, demo, **kwargs)


class LoginsMonitor(CoreMonitor[LoginsInfo, CoreMonitorConfig]):
    def _init_settings(
        self, debug_mode: bool, force_cache: bool
    ) -> CoreMonitorSettings[CoreMonitorConfig]:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic=SocketTopic.LOGINS,
            config=CoreMonitorConfig("monitor.logins", debug_mode, force_cache),
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[LoginsInfo]) -> pt.Text:
        val = len(msg.data.parsed)

        val_st = Styles.TEXT_DISABLED
        label_st = Styles.TEXT_DISABLED
        if val > 1:
            val_st = Styles.TEXT_UPDATED
            label_st = Styles.VALUE_LBL_5

        label_pfx = "("
        label_sfx = ")"
        val_str = str(val)
        val_fg = pt.Fragment(val_str.rjust(1), val_st)
        if len(val_str) > 1:
            label_st = Styles.TEXT_VALUE_OVERFLOW_LABEL
            val_fg = format_value_overflow(1)

        return pt.Text(
            pt.Fragment(label_pfx, label_st),
            val_fg,
            pt.Fragment(label_sfx, label_st),
        )
