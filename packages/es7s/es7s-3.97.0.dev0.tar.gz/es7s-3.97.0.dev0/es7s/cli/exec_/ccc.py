# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from .._base_opts_params import EnumChoice, HelpPart
from .._decorators import cli_command, catch_and_log_and_exit, cli_flag, cli_option
from es7s.shared.enum import GraphOutputFormat


fmt_choice = EnumChoice(GraphOutputFormat, inline_choices=True)


@cli_command(__file__, "&crypto&currency &chart")
@cli_option(
    "-f",
    "--format",
    type=fmt_choice,
    default=GraphOutputFormat.CLI,
    show_default=True,
    help="Output format selection.",
)
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Fetch cryptocurrencies statistics for the past 24h and
    display sorted by market capacity.
    """
    from es7s.cmd.ccc import action

    action(**kwargs)
