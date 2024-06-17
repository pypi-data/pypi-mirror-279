# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from ..._base import CliCommand
from ..._base_opts_params import CMDTRAIT_ADAPTIVE_OUTPUT, CMDTYPE_BUILTIN
from ..._decorators import catch_and_log_and_exit, cli_command


@cli_command(
    name=__file__,
    cls=CliCommand,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE_OUTPUT],
    short_help="internal inspect method demo output",
)
@catch_and_log_and_exit
class invoker:
    """
    Display internal `inspect` method invocation result.\n\n
    """

    def __init__(self, **kwargs):
        from es7s.cmd.print_demo_inspect import action

        action(**kwargs)
