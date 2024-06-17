# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from .._base_opts_params import EnumChoice, CMDTRAIT_X11
from .._decorators import (
    catch_and_log_and_exit,
    cli_option,
    cli_argument,
    cli_command,
)
from ...shared.enum import EventStyle


@cli_command(__file__, "send a notification", traits=[CMDTRAIT_X11])
@cli_argument("ident")
@cli_argument("message")
@cli_option(
    "-s",
    "--style",
    type=EnumChoice(EventStyle, inline_choices=True),
    default=EventStyle.INFO,
    show_default=True,
    metavar="NAME",
    help="Event style.",
)
@catch_and_log_and_exit
def invoker(*args, **kwargs):
    """
    @TODO fix click ARGUMENT output
    """
    from es7s.cmd.notify import action

    action(*args, **kwargs)
