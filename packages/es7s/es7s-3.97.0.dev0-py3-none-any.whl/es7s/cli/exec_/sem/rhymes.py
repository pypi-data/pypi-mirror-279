# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from es7s.shared.enum import WordType
from ..._base_opts_params import EnumChoice, IntRange
from ..._decorators import catch_and_log_and_exit, cli_command, cli_argument, cli_flag, cli_option
import pytermor as pt


@cli_command(__file__, "find rhymes")
@cli_argument("word", nargs=1, required=True)
@cli_flag("-r", "--raw", help="Display raw HTML content.")
@cli_flag(
    "-n",
    "--no-input",
    help="Do not prompt for next page(s); gets enabled automatically when stdin is not a tty.",
)
@cli_flag(
    "-S",
    "--same-size",
    help="Show only results with same number of syllables as WORD; equivalent to specifying "
    "'-s' manually.",
)
@cli_option(
    "-s",
    "--size",
    type=IntRange(1),
    help="Show only results consisting of N syllables. [default: show all]",
    default=None,
)
@cli_option(
    "-t",
    "--type",
    "_type",
    type=EnumChoice(WordType),
    help="Show only results of specified type. [default: show all] ["
    + "|".join(pt.render(k, v) for (k, v) in WordType.styles().items())
    + "]",
    default=None,
    metavar="TYPE",
)
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Query external service for rhymes to specified WORD.\n\n

    Remote service is ++rifmovka.ru++
    """
    from es7s.cmd.sem import action_rhymes as action

    action(**kwargs)
