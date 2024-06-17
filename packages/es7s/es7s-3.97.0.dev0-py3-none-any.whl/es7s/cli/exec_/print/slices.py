# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from ..._base_opts_params import CMDTYPE_BUILTIN, IntRange, CMDTRAIT_ADAPTIVE_OUTPUT
from ..._decorators import cli_command, cli_option, catch_and_log_and_exit


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE_OUTPUT],
    short_help="print python slices example table",
)
@cli_option(
    "-n",
    "--length",
    type=IntRange(1, 64),
    help="autogenerate sample with specified length",
)
@cli_option("-s", "--sample", help="string to use as a sample, disables sample autogeneration")
@catch_and_log_and_exit
class invoker:
    """
    Print example table with results of applying Python's string slice operation
    "sample[<<begin>>:<<end>>:<<step>>]" with all combinations of <<begin>> and <<end>> and two
    various <<step>>s.\n\n

    @A> The terminal size determines maximum table size and consequently the length
    of the sample if no args are specified. The algorithm calculates the longest
    sample that will produce a table that will fit into current terminal both by
    width and height.
    """

    def __init__(self, **kwargs):
        from es7s.cmd.print_slices import action

        action(**kwargs)
