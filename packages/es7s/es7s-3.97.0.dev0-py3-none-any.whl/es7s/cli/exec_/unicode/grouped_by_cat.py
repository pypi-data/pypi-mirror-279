# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from ..._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_NONE, CharIntRange
from ..._decorators import cli_command, catch_and_log_and_exit, cli_option


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_NONE],
    short_help="display unicode codepoints from specified range grouped by category",
)
@cli_option(
    "-s",
    "--start",
    type=CharIntRange(),
    default=0,
    show_default=True,
    help="Range start codepoint code",
)
@cli_option(
    "-e",
    "--end",
    type=CharIntRange(),
    default=0x7E,
    show_default=True,
    help="Range end codepoint code",
)
@catch_and_log_and_exit
class invoker:
    """
    Display unicode codepoints from specified range grouped by category
    (inclusive).
    """

    def __init__(self, **kwargs):
        from es7s.cmd.print_unicode_grouped import action

        action(**kwargs)
