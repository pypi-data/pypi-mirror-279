# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

from .._base_opts_params import CMDTRAIT_ADAPTIVE_OUTPUT, CMDTYPE_BUILTIN
from .._decorators import (
    catch_and_log_and_exit,
    cli_command,
    cli_argument,
)


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE_OUTPUT],
    short_help="&(auto)-process-&(term)inator",
)
@cli_argument(
    "filter",
    nargs=1,
    from_config="default-filter",
    default="vlc",
)
@catch_and_log_and_exit
def invoker(*args, **kwargs):
    """
    The application is designed for automatic/manual termination of processes
    matching the specified regular expression (=''filter''), by pressing [t] key
    once for each process, or by pressing [T], which terminates ALL displayed
    processes. In the first case the signal is sent to the topmost process in
    the list, while processes are sorted by CPU usage.\n\n

    Another option is to enable the auto-termination mechanism, which will send
    SIGTERM to all processes matching the filter as soon as they are detected.
    This can be done by pressing [A] key; pressing it again will switch the
    application back to manual control.\n\n

    Process table columns: PID, NAME, CPU, MEM, IO read total and delta,
    write total and delta.
    """
    from es7s.cmd.autoterm import action

    action(*args, **kwargs)
