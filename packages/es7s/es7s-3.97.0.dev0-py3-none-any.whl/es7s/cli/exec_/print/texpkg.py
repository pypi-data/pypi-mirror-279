# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from es7s.cli._base_opts_params import CMDTYPE_UNBOUND
from ..._base import CliCommand
from ..._base_opts_params import CMDTRAIT_ADAPTIVE_OUTPUT
from ..._decorators import catch_and_log_and_exit, cli_option, cli_command


@cli_command(
    name=__file__,
    cls=CliCommand,
    type=CMDTYPE_UNBOUND,
    traits=[CMDTRAIT_ADAPTIVE_OUTPUT],
    short_help="TeX packages version list",
)
@cli_option(
    "-f",
    "--full",
    is_flag=True,
    default=False,
    help="Do not collapse any fields.",
)
@cli_option(
    "-s",
    "--source",
    is_flag=True,
    default=False,
    help="Print.",
)
@catch_and_log_and_exit
class invoker:
    """
    Search for installed LaTeX packages ('*.sty') and make an attempt to
    determine a version of each, then display the results as a list.
    """

    PAD = " " * 1

    def __init__(self, **kwargs):
        from es7s.cmd.print_texpkg import action

        action(**kwargs)
