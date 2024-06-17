# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import click

from es7s.shared.enum import RepeatedMode
from ..._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_NONE, HelpPart
from ..._decorators import cli_command, catch_and_log_and_exit, cli_option, cli_argument


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_NONE],
    short_help="list of executables resolved from @PATH@",
    interlog=[
        HelpPart(
            "Deduplication mode:",
        ),
        HelpPart(
            "⏺ “active” enforces the application to show only first (effective) path while "
            "omitting all repeated ones.",
            indent_shift=1,
        ),
        HelpPart(
            "⏺ “groups” mode merges repeated paths into groups, just as 'active' does, but "
            "also displays the amount of duplicates in each squashed path."
            "[this is a default].",
            indent_shift=1,
        ),
        HelpPart(
            "⏺ “all” mode disables all merging: each record is displayed regardless of "
            "the repeat count.",
            indent_shift=1,
        ),
    ],
)
@cli_argument("filter", nargs=-1, required=False)
@cli_option(
    "-m",
    "--mode",
    type=click.Choice(RepeatedMode.list()),
    default=RepeatedMode.GROUPS,
    help="Deduplication mode (see above).",
)
@cli_option("-f", "--full-chain", is_flag=True, help="Do not collapse symlink chains.")
@catch_and_log_and_exit
class invoker:
    """
    List all executables accessible from the shell, optionally count or group
    duplicate (i.e., conflict) names. FILTERs are treated like substrings, and
    any of them must be present in executable's name in order to be displayed.
    If no FILTERs defined, do not filter the result list.
    """

    def __init__(self, **kwargs):
        from es7s.cmd.print_bin import action

        action(**kwargs)
