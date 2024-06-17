# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from .._base_opts_params import CMDTRAIT_ADAPTIVE_OUTPUT, CMDTRAIT_ADAPTIVE_INPUT
from .._decorators import (
    catch_and_log_and_exit,
    cli_argument,
    cli_command,
    cli_flag,
    cli_option,
    cli_adaptive_input,
)


@cli_command(
    __file__,
    "SGR-aware text to columns splitter",
    traits=[CMDTRAIT_ADAPTIVE_INPUT, CMDTRAIT_ADAPTIVE_OUTPUT],
)
@cli_adaptive_input(demo=True, input_args=False)
@cli_flag("-X", "--rows-first", help="Fill table horizontally rather than vertically.")
@cli_option("-g", "--gap", help="Number of spaces between columns.", default=1, show_default=True)
@cli_option("-t", "--tabsize", help="Width of a tab stop to set up.", default=8, show_default=True)
@cli_option(
    "-s",
    "--sectsize",
    help="Number of lines in each section (0=disable sections).",
    default=0,
    show_default=True,
)
@cli_option(
    "-G", "--sectgap", help="Number of newlines between sections.", default=1, show_default=True
)
@catch_and_log_and_exit
def invoker(*args, **kwargs):
    """
    Read text from given FILENAME and display it split into columns. If FILENAME is omitted
    or equals to ''-'', read standard input instead.\n\n

    Amount of columns is determined automatically depending on original lines maximum
    length and @A> terminal width.
    """
    from es7s.cmd.columns import action

    action(**kwargs)
