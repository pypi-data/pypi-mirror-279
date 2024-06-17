# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from ..._decorators import catch_and_log_and_exit, cli_command


@cli_command(__file__, "list es7s daemon sockets")
@catch_and_log_and_exit
class invoker:
    """
    Print a list of valid socket topics.
    """

    def __init__(self, **kwargs):
        from es7s.cmd.socket_ import action_list as action

        action(**kwargs)
