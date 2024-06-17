# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023-2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from datetime import datetime

from .._base_opts_params import (
    CMDTRAIT_ADAPTIVE_OUTPUT,
    MonthYearType,
    CMDTYPE_DRAFT,
)
from .._decorators import cli_command, cli_option, catch_and_log_and_exit, cli_argument


@cli_command(
    __file__,
    type=CMDTYPE_DRAFT,
    traits=[CMDTRAIT_ADAPTIVE_OUTPUT],
    short_help="print a calendar of current/specified month/year",
    interlog=MonthYearType.get_format_section(),
    command_examples=[
        ("Current month:", "{}"),
        ("Current year:", "{} -f"),
        ("For Dec 2024:", "{} dec-2024"),
        ("For 2025:", "{} -f 2025"),
    ],
)
@cli_argument(
    "dt",
    type=MonthYearType(),
    nargs=1,
    default=lambda: datetime.now().strftime(next(iter(MonthYearType.get_formats()))),
)
@cli_option(
    "-f",
    "--full",
    is_flag=True,
    help="Display calendar of a whole year instead of just one month.",
)
@catch_and_log_and_exit
class invoker:
    """
    Display a calendar of specified month or specified year. If omimtted, the
    current month and/or year are used instead.
    """

    def __init__(self, **kwargs):
        from es7s.cmd.cal import action

        action(**kwargs)
