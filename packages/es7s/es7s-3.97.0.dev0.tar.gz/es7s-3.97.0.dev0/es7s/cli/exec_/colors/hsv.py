# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import typing

from ..._base import CliCommand
from ..._base_opts_params import CMDTRAIT_ADAPTIVE_OUTPUT
from ..._decorators import catch_and_log_and_exit, cli_command, cli_option

_T = typing.TypeVar("_T")


@cli_command(
    name=__file__,
    cls=CliCommand,
    short_help="xterm-256 colors as HSV table",
    traits=[CMDTRAIT_ADAPTIVE_OUTPUT],
)
@cli_option(
    "--compact/--wide",
    is_flag=True,
    default=None,
    help="Force compact mode even if terminal is wide enough for widescreen mode, or force widescreen "
    "mode even if the content will not fit by width.",
)
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Display ++xterm-256++ color chart (with ++xterm-16++ as a part of it)
    aligned using HSV channel values for easier color picking.
    """
    from es7s.cmd.colors_hsv import action

    action(**kwargs)
