# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import math

import pytermor as pt

from es7s.shared import RulerType
from ..._base_opts_params import CMDTRAIT_ADAPTIVE_OUTPUT, IntRange, EnumChoice
from ..._base_opts_params import FloatRange
from ..._base_opts_params import HelpPart
from ..._decorators import catch_and_log_and_exit, cli_command
from ..._decorators import cli_option

_cmd_epilog = HelpPart(
    pt.pad(5).join(
        f'{"*"+rt+"*":s} = {k.name.lower().replace("_", " ").capitalize()}'
        for (k, rt) in RulerType.dict().items()
    )
    + "\n\n  ",
    "Ruler types",
)


@cli_command(
    __file__, "terminal char rulers", traits=[CMDTRAIT_ADAPTIVE_OUTPUT], epilog=[_cmd_epilog]
)
@cli_option(
    "-R",
    "--no-rulers",
    is_flag=True,
    default=False,
    help="Disable all rulers. If '-R' is specified, all '-r' options will be ignored.",
)
@cli_option(
    "-r",
    "--rulers",
    type=EnumChoice(RulerType, inline_choices=True),
    default=RulerType.DEFAULT(),
    show_default=True,
    multiple=True,
    metavar="TYPE",
    help="Which rulers to draw. Can be specified multiple times: '-r B -r L' "
    "will result in drawing two rulers -- bottom and left. The legend for "
    "ruler types can be found below.",
)
@cli_option(
    "-p",
    "--position",
    type=FloatRange(_min=-math.inf, _max=math.inf, min_open=True, max_open=True),
    default=0.5,
    show_default=True,
    help="Position of center horizontal line (should be enabled with '-r CH'). "
    "Can be specified as a float number from 0.0 to 1.0, in which case the "
    "value is treated like relative position to the screen height (e.g. "
    "0.25=25%), or as an integer number representing the distance from the "
    "top side of the screen (in lines) to the ruler. For negative values "
    "logic is the same, except the reference side of the screen is bottom "
    "one instead of the top.",
)
@cli_option(
    "-g",
    "--grid",
    type=IntRange(0, 3, clamp=True),
    default=2,
    show_default=True,
    help="Grid details level.",
)
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Draw four rulers at the top, bottom, left and right sides of the terminal and
    additionally draw a grid with specified details level.
    """
    from es7s.cmd.print_rulers import action

    action(**kwargs)
