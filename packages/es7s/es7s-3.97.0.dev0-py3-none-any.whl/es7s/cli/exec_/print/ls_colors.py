# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from es7s.cli._base_opts_params import CMDTRAIT_ADAPTIVE_OUTPUT
from ..._base_opts_params import CMDTYPE_BUILTIN
from ..._decorators import cli_command, catch_and_log_and_exit, cli_option


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE_OUTPUT],
    short_help="all colors defined in @LS_COLORS@ as applied examples",
)
@cli_option("-x", "--extend", is_flag=True, help="Display detailed list instead of grid.")
@cli_option(
    "-X", "--rows-first", is_flag=True, help="Fill table horizontally rather than vertically."
)
@cli_option("--sort-by-color", is_flag=True, help="Print entries grouped by color.")
@catch_and_log_and_exit
class invoker:
    """
    Extract all rules described in @LS_COLORS@, build an artificial list of names matching
    each of these, apply the corresponding rules and display as a grid, or as a detailed
    list (with '-x').
    """

    def __init__(self, **kwargs):
        from es7s.cmd.print_ls_colors import action

        action(**kwargs)
