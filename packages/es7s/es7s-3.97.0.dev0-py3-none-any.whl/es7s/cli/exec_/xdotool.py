# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from .._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_X11, FloatRange
from .._decorators import cli_command, cli_argument, catch_and_log_and_exit, cli_option


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_X11],
    short_help="run specified xdotool command(s) or preset(s)",
    command_examples=[
        "{} -t 5 chrome-img-to-tg chrome-close-tab",
        "{} -L -- search --onlyvisible --sync --class telegram windowraise",
    ],
    ignore_unknown_options=True,
    allow_extra_args=True,
)
@cli_argument(
    "args",
    type=str,
    required=True,
    nargs=-1,
)
@cli_option(
    "-L",
    "--literal",
    is_flag=True,
    help="Treat ARGs as 'xdotool' commands, not as preset filenames.",
)
@cli_option(
    "-t",
    "--timeout",
    type=FloatRange(_min=0.0, max_open=True, show_range=False),
    default=0.0,
    help="Set maximum execution time for all the commands *combined*. 0 is "
    "unlimited [which is a default].",
)
@catch_and_log_and_exit
class invoker:
    """
    Read 'xdotool' preset file(s) with names specified as ARGS and run the
    content of each of these like a command list; or (with '-L') pass the
    ARGS to 'xdotool' like commands directly.\n\n

    In the latter case it\\'s recommended to separate the argument list with
    '--' in order to avoid possible collisions between 'es7s' options and
    ones that are meant for 'xdotool'.\n\n

    This command requires [[x11]] environment and also requires
    ++/usr/bin/xdotool++ to be present and available.
    """

    def __init__(self, **kwargs):
        from es7s.cmd.xdotool import action

        action(**kwargs)
