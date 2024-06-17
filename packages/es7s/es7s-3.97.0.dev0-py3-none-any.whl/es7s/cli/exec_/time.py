# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations
from .._base_opts_params import CMDTRAIT_ADAPTIVE_OUTPUT, IntRange, HelpPart
from .._decorators import (
    catch_and_log_and_exit,
    cli_option,
    cli_command,
    cli_flag,
    cli_full_terminal,
)


@cli_command(
    __file__,
    "display system time",
    traits=[CMDTRAIT_ADAPTIVE_OUTPUT],
    epilog=[
        HelpPart(
            [
                ("&[r]efresh", "Redraw the screen"),
                (
                    "&[f]ormat",
                    "Cycle through formats: HH:MM, HH:MM:SS, <<custom>>",
                ),
                ("&[i]ntensity", "Adjust character brightness"),
                ("&[z]oom", "Change scale factor"),
                ("&[w]ide/narrow", "Toggle between single- and double-character output."),
                ("&[t]extcolor", "Cycle through basic colors"),
                ("&[D]ebug", "Toggle debug mode"),
                ("&[q]uit", "Exit the application"),
            ],
            title="Controls:",
        ),
    ],
)
@cli_full_terminal
@cli_flag(
    "-s", "--seconds", show_default=True, help="Display seconds by default; alias for '*-f* %T'."
)
@cli_option(
    "-f",
    "--format",
    default="%R",
    show_default=True,
    help="Override output format written in python\\'s 'strftime' syntax, which in general "
    "matches GNU date format syntax.",
)
@cli_option(
    "-t",
    "--text-color",
    metavar="CDT",
    help="Text color name or RGB value in 0xRRGGBB form. [default: theme color]",
)
@cli_option(
    "--intensity",
    type=IntRange(_min=1, _max=4),
    default=4,
    show_default=True,
    help="Character brightness, also selectable with &[i] key.",
)
@cli_flag(
    "--narrow",
    help="Use a single block for output \\'pixel\\' (toggle with &[n]).  [default: double block]",
)
@cli_flag("--debug", show_default=True, help="Enable debug mode (toggle with &[d]).")
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Display system time using large digits (suggested usage is terminal fullscreen mode).
    """
    from es7s.cmd.time import action

    action(**kwargs)
