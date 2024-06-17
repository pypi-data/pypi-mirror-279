# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click
import pytermor as pt

from es7s.shared import ShocksInfo
from es7s.shared import SocketMessage, SocketTopic
from es7s.shared import Styles as S
from es7s.shared.styles import format_value_overflow
from ._base import (
    CoreMonitor,
    MonitorCliCommand,
    CoreMonitorSettings,
    CoreMonitorConfig,
)
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command

OUTPUT_WIDTH = 7


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="SSH/SOCKS proxy tunnels count",
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    ShocksMonitor(ctx, demo, **kwargs)


class ShocksMonitor(CoreMonitor[ShocksInfo, CoreMonitorConfig]):
    def _init_settings(
        self, debug_mode: bool, force_cache: bool
    ) -> CoreMonitorSettings[CoreMonitorConfig]:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic=SocketTopic.SHOCKS,
            network_comm_indic=True,
            config=CoreMonitorConfig("monitor.shocks", debug_mode, force_cache),
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[ShocksInfo]) -> pt.Text:
        # st_updated = pt.Style(S.TEXT_UPDATED, blink=True)
        st_updated = [S.TEXT_UPDATED,S.TEXT_DISABLED][self._state.tick_render_num % 2]
        # fmt: of8f
        val_upstream =     msg.data.tunnel_amount or 0
        val_relay_active = msg.data.relay_connections_amount or 0
        val_relay_listen = msg.data.relay_listeners_amount or 0
        server_mode =      bool(val_relay_active or val_relay_listen)
        upstream_cmp =     self._make_fragment(val_upstream, bool(val_upstream), label="T", label_st=S.VALUE_LBL_5)
        relay_active_cmp = self._make_fragment(val_relay_active, server_mode, active_st=st_updated, label="/")
        relay_listen_cmp = self._make_fragment(val_relay_listen, server_mode, label="R", label_st=S.VALUE_LBL_5)
        # fmt: on

        return pt.Text(
            upstream_cmp,
            " ",
            relay_active_cmp,
            relay_listen_cmp,
        )

    def _make_fragment(
        self,
        val: int,
        enabled=True,
        *,
        active_st=S.VALUE_PRIM_1,
        inactive_st=S.WARNING,
        disabled_st=S.TEXT_DISABLED,
        label: str = None,
        label_st=S.TEXT_DISABLED,
    ) -> pt.Composite:
        result = pt.Composite()

        val_str = str(val)
        if len(val_str) > 1:
            result += format_value_overflow(1)
            if label:
                result += pt.Fragment(label, S.TEXT_VALUE_OVERFLOW_LABEL)
            return result

        st = disabled_st
        if enabled:
            st = [inactive_st, active_st][bool(val)]

        result += pt.Fragment(val_str, st)
        if label:
            result += pt.Fragment(label, label_st)
        return result
