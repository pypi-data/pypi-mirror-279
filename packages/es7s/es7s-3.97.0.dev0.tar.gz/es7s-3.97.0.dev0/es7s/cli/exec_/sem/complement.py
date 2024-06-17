# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from ..._decorators import catch_and_log_and_exit, cli_command, cli_argument, cli_flag


@cli_command(__file__, "find complement words")
@cli_argument("word", nargs=-1, required=True)
@cli_flag("-r", '--raw', help="Display raw HTML content")
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Query external service for a complement words to each of specified WORDs.
    """
    from es7s.cmd.sem import action_complement as action

    action(**kwargs)
