# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from .._base_opts_params import IntRange
from .._decorators import (
    catch_and_log_and_exit,
    cli_command,
    cli_flag,
    cli_adaptive_input,
    AdaptiveInputWithDemoAttrs,
    cli_option,
)


@cli_command(
    __file__,
    short_help="find shortest merge combination of INPUTs",
    **AdaptiveInputWithDemoAttrs,
)
@cli_adaptive_input(demo=True)
@cli_option(
    "-s",
    "--max-size",
    type=IntRange(1),
    default=5,
    show_default=True,
    help="How many INPUTs should output be composed of.",
)
@cli_option(
    "-o",
    "--min-overlap",
    type=IntRange(1),
    default=2,
    show_default=True,
    help="Minimum number of letters in parts shared by two adjacent INPUTs.",
)
@cli_flag(
    "-N",
    "--nesting",
    help="Allows an INPUT to be fully included in next INPUT "
    "[default: require all INPUTs to have at least one non-shared "
    "letter, or to consist of shared letters belonging to two "
    "different adjacent parts]",
)
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Find shortest combination of INPUT lines of specified length by performing
    a merge of common parts of adjacent words into each other.
    """
    from es7s.cmd.word_combiner import action

    action(**kwargs)
