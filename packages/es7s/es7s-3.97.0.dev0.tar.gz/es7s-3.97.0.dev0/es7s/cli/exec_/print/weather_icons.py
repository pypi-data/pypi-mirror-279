# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from ..._base_opts_params import CMDTRAIT_ADAPTIVE_OUTPUT
from ..._decorators import catch_and_log_and_exit, cli_option, cli_command


@cli_command(__file__, "weather icon table display/measure", traits=[CMDTRAIT_ADAPTIVE_OUTPUT])
@cli_option(
    "-m",
    "--measure",
    is_flag=True,
    default=False,
    help="Also perform a character width measuring.",
)
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Print weather icons used in `es7s/monitor`.
    """
    from es7s.cmd.print_weather_icons import action

    action(**kwargs)
