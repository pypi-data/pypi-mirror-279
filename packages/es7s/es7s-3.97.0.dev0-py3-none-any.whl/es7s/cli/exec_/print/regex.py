# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from ..._base_opts_params import CMDTRAIT_ADAPTIVE_OUTPUT
from ..._decorators import catch_and_log_and_exit, cli_command


@cli_command(__file__, "python regular expressions", traits=[CMDTRAIT_ADAPTIVE_OUTPUT])
@catch_and_log_and_exit
class invoker:
    """
    Display python regular expressions cheatsheet.\n\n

    For best results view it on a terminal at least 180 characters wide, although
    anything down to 88 chars is good enough, too. Consider piping the output to
    a pager if width of your terminal is less than that. Use '-c' option to force
    formatting in the output, because the app disables it by default, if detects
    a pipe or redirection.
    """

    def __init__(self, **kwargs):
        from es7s.cmd.print_regex import action

        action(**kwargs)
