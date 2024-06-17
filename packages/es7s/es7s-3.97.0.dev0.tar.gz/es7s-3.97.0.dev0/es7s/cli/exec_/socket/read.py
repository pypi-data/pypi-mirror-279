# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import random

from es7s.shared.enum import SocketTopic
from ..._base_opts_params import EnumChoice
from ..._decorators import catch_and_log_and_exit, cli_command, cli_argument, cli_flag


@cli_command(
    __file__,
    short_help="read data provided by es7s/daemon",
    command_examples=["{} " + random.choice(SocketTopic.list())],
)
@cli_argument("topic", type=EnumChoice(SocketTopic), metavar="TOPIC")
@cli_flag("-r", "--raw", help="Do not deserialize data from socket")
@catch_and_log_and_exit
class invoker:
    """
    Read data from a socket with specified topic and display it.
    """

    def __init__(self, **kwargs):
        from es7s.cmd.socket_ import action_read as action

        action(**kwargs)
