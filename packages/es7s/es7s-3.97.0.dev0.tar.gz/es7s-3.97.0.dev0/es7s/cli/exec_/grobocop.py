# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from es7s.cli._decorators import cli_flag
from .._base_opts_params import HelpPart
from es7s.shared import GrobocopStyles
from .._decorators import cli_command, cli_argument, catch_and_log_and_exit

import pytermor as pt

__styles = GrobocopStyles()
_legend_st = lambda st: pt.merge_styles(st, fallbacks=[pt.Style(bg=pt.cv.GRAY_0)])


@cli_command(
    __file__,
    "&g&rid-aligned &o&bs&olete &c&ode&pages",
    interlog=[
        HelpPart(
            [
                (pt.Fragment(" A ", _legend_st(__styles.DEFAULT)), "Regular character"),
                (pt.Fragment("NUL", _legend_st(__styles.CC)), "Control character"),
                (pt.Fragment("NBS", _legend_st(__styles.WS)), "Whitespace character"),
                (pt.Fragment(" § ", _legend_st(__styles.OVERRIDE)), "Override DOS character"),
                (pt.Fragment(" ð ", _legend_st(__styles.MULTIBYTE)), "Example multibyte char."),
                (pt.Fragment(" ? ", _legend_st(__styles.UNASSIGNED)), "Unassigned codepoint"),
                (pt.Fragment(" ? ", _legend_st(__styles.ERROR)), "Invalid codepoint"),
                (pt.Fragment(" FF", _legend_st(__styles.UNDEFINED)), "No mapping"),
            ],
            title="Legend:",
        ),
    ],
)
@cli_argument("codepage", type=str, required=False, nargs=-1)
@cli_flag(
    "-l", "--list", help="Display list of supported CODEPAGEs (plus aliases with '--all') and exit."
)
@cli_flag(
    "-a",
    "--all",
    help="Ignore CODEPAGE argument(s) and display all supported code pages at once.",
)
@cli_flag("-w", "--wide", help="Use wider table cells.")
@cli_flag(
    "-u",
    "--codes",
    help="Display Unicode code point numbers instead of characters (implies '--wide').",
)
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Display bytes from range [0x00; 0xFF] encoded using specified CODEPAGE(s). If no CODEPAGE argument
    is provided, use 'ascii' code page. List of supported code pages can be seen with '-l'.
    """
    from es7s.cmd.grobocop import action

    action(**kwargs)
