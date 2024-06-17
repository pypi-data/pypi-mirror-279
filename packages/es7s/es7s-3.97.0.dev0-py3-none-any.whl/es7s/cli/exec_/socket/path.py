# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import random

from es7s.shared.enum import SocketTopic
from ..._base_opts_params import EnumChoice
from ..._decorators import catch_and_log_and_exit, cli_command, cli_argument


@cli_command(
    __file__,
    short_help="get es7s daemon sockets path",
    command_examples=["{} " + random.choice(SocketTopic.list())],
)
@cli_argument("topic", type=EnumChoice(SocketTopic), metavar="TOPIC")
@catch_and_log_and_exit
class invoker:
    """
    Return path to a file which is used as a socket for interprocess
    communication between es7s/daemon and es7s monitors, by socket topic.
    """

    def __init__(self, **kwargs):
        from es7s.cmd.socket_ import action_path as action

        action(**kwargs)
