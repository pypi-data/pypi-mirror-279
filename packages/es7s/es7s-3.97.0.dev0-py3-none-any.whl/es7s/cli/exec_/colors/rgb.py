# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

from ..._base import CliCommand
from ..._base_opts_params import IntRange
from ..._decorators import catch_and_log_and_exit, cli_command, cli_option


@cli_command(name=__file__, cls=CliCommand, short_help="rgb spectre")
@cli_option("-i", "--invert", default=False, is_flag=True, help="Use inverted colors.")
@cli_option(
    "-w",
    "--width",
    default=77,
    show_default=True,
    type=IntRange(_min=3, max_open=True),
    help="Gradient width, in characters.",
)
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Display RGB color gradient.
    """
    from es7s.cmd.colors_rgb import action
    action(**kwargs)
