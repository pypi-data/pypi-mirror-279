# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

from .._base_opts_params import (
    CMDTRAIT_ADAPTIVE_OUTPUT,
    FloatRange,
    IntRange,
    DayMonthType,
)
from .._decorators import catch_and_log_and_exit, cli_option, cli_command


@cli_command(
    __file__,
    "display sunrise and sunset timings",
    command_examples=[
        "{} --date Nov-15",
        "{} --date 11-15",
        "{} --date 15-Nov --lat 52.12 --long 36.32",
        "{} --date 15nov --lat 90.00 --long 00.00",
    ],
    interlog=DayMonthType.get_format_section(),
    traits=[CMDTRAIT_ADAPTIVE_OUTPUT],
)
@cli_option(
    "-d",
    "--date",
    type=DayMonthType(),
    show_default="current",
)
@cli_option(
    "-φ",
    "--lat",
    type=FloatRange(-90, 90),
    default=55.755833,
    show_default=True,
    help="A coordinate that specifies the north–south position of a point of interest.",
)
@cli_option(
    "-λ",
    "--long",
    type=FloatRange(-180, 180),
    default=37.617222,
    show_default=True,
    help="A coordinate that specifies the east–west position of a point of interest.",
)
@cli_option(
    "-A",
    "--auto-update",
    is_flag=True,
    show_default=True,
    help="Enable auto-update infinite loop mode.",
)
@cli_option(
    "-m",
    "--margin",
    type=IntRange(0, max_open=True),
    default=1,
    show_default=True,
    help="Number of spaces on each side of the output.",
)
@cli_option(
    "-i",
    "--interval",
    type=FloatRange(0.0, max_open=True),
    default=1.0,
    show_default=True,
    help="Delay between frame renderings. Ignored if not an auto-update mode.",
)
@cli_option(
    "--no-emoji",
    is_flag=True,
    help="Replace time of the day emoji icons with color squares.",
)
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    @TODO curl ip-api.com -> geolocation [timeout 1s, disablable]
    """
    from es7s.cmd.sun import action

    action(**kwargs)
