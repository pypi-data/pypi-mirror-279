# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from typing import cast

import click

from es7s.shared import get_stdout
from ..._base import CliGroup
from ..._decorators import catch_and_log_and_exit, cli_command, cli_pass_context


@cli_command(__file__, "command index and prolog")
@cli_pass_context
@catch_and_log_and_exit
def invoker(ctx: click.Context, **kwargs):
    """
    Display F.A.N command list and prolog.
    """
    cmd_group = cast(CliGroup, ctx.parent.command)
    cmd_prolog = cmd_group.get_command(ctx, "prolog")

    ctx.invoke(cmd_prolog)

    fmtr = ctx.make_formatter()
    cmd_group.format_commands(ctx, fmtr)
    get_stdout().echo(fmtr.getvalue())
