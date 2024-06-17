# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from .._base_opts_params import IntRange
from .._decorators import (
    catch_and_log_and_exit,
    cli_option,
    cli_argument,
    cli_command,
    cli_adaptive_input,
)


@cli_command(
    name=__file__,
    short_help="SGR-aware text folding to specified width",
)
@cli_adaptive_input(demo=True)
@cli_option(
    "-w",
    "--max-width",
    type=IntRange(_min=0),
    default=120,
    show_default=True,
    help="Set maximum length of one line of the output. Actual value can be smaller, e.g., when output is a "
    "terminal narrower than N characters. Also, 2 more spaces are added to lower the chances that characters with "
    "incorrect width will break the wrapping. Setting to 0 disables the limit.",
)
@cli_option(
    "-W",
    "--force-width",
    type=IntRange(_min=1),
    help="Force output lines to be N characters wide no matter what device/program is receiving it.",
)
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Read text from given FILE and wrap it to specified width. If FILE is omitted
    or equals to ''-'', read standard input instead.\n\n

    Works like standard python's `textwrap.wrap()`, except that it takes into account
    terminal control sequences (i.e. SGRs).
    """
    from es7s.cmd.wrap import action

    action(**kwargs)
