# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import pathlib

from es7s.shared import with_progress_bar
from ..._base_opts_params import IntRange
from ..._decorators import (
    cli_argument,
    cli_command,
    cli_option,
    catch_and_log_and_exit,
)


@cli_command(__file__, "Launch a demonstration of ProgressBar CLI component.")
@cli_option(
    "-s",
    "--slower",
    default=1,
    help="Add an artificial delay of eⁿ seconds between operations."
    " By default (n=0) no delay is applied. n=1 sets the delay to ≈3ms, "
    "n=5 to ≈140ms, n=10 to ≈21sec. Reasonable slow levels "
    "are within range [1;5], others make the execution process look "
    "like step debugging.",
    type=IntRange(_min=0, _max=10),
)
@cli_option(
    "-f",
    "--faster",
    default=False,
    is_flag=True,
    help="Override any delays set by '--slower' option and furthermore "
    "speed up the execution by disabling file headers reading.",
)
@cli_argument("path", default="/home", type=pathlib.Path)
@catch_and_log_and_exit
@with_progress_bar(print_step_num=True)
def invoker(*args, **kwargs):
    """ """
    from es7s.cmd.print_demo_progress_bar import action
    action(*args, **kwargs)
