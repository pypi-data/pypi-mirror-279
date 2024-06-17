# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from es7s.cli._decorators import cli_adaptive_input
from ..._base_opts_params import CMDTRAIT_ADAPTIVE_OUTPUT, IntRange
from ..._decorators import catch_and_log_and_exit, cli_command, cli_option


@cli_command(
    __file__,
    "Launch a demonstration of Gradient component.",
    traits=[CMDTRAIT_ADAPTIVE_OUTPUT],
    # @FIXME add shared AdaptiveInputAttrs
)
@cli_adaptive_input(demo=True, input_args=False)
@cli_option(
    "-h",
    "--height",
    type=IntRange(1, max_open=True, show_range=False),
    default=1,
    show_default=True,
    help="Gradient scale height in characters.",
)
@cli_option(
    "-x",
    "--extend",
    type=IntRange(0, 3, clamp=True, show_range=False),
    default=0,
    count=True,
    help="Display detailed info about gradient segments. Can be used multiple times to increase "
    "the details amount even further ('-xx', '-xxx').",
)
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Read data from given specified FILENAME, build and display a gradient based on it.
    The only supported format is GIMP gradient (**.ggr*). If no '-F', '-S' or
    '-d' option is provided, read standard input. Multiple FILENAMEs supported.
    """
    from es7s.cmd.print_gradient import action

    action(**kwargs)
