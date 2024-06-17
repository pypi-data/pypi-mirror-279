# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from es7s.shared.enum import EsqDbMode
from .._base_opts_params import EnumChoice, FloatRange
from .._decorators import cli_argument, cli_command, cli_option, cli_flag


@cli_command(
    __file__,
    "&escape &se&q &de&bugger, interactive step-by-step stream inspector",
    usage_override=[
        "send [INFILE [OUTFILE]]",
        "recv [INFILE]",
        "--help",
    ],
    command_examples=[
        "1. read the output of a command through pipe broken down by escape seqs (no control terminal):",
        "",
        "     <<...>> | {} send - /dev/null",
        "",
        "2. stream breakdown+assembly (two terminals, 2nd is control one) communicating over a named pipe,",
        "   (which is set up by the application in the background if no arguments specified):",
        "",
        "     <<...>> | {} send",
        "     {} recv",
        "",
        "3. stream breakdown+assembly communicating over a file, which keeps the transmitted data:",
        "",
        "     <<...>> | {} send - /tmp/esq",
        "     tail -f /tmp/esq | {} recv",
        "",
        "4. step-by-step (manual control) breakdown+assembly from a file:",
        "",
        "     {} send /tmp/esq",
        "     {} recv",
        "",
        "5. similar to (4), but the same terminal is used for code display and as a control one (results may vary):",
        "",
        "     {} send /tmp/esq -",
    ],
)
@cli_argument("mode", type=EnumChoice(EsqDbMode, show_choices=True), required=True)
@cli_argument("infile", type=click.File(mode="rb"), required=False)
@cli_argument("outfile", type=click.File(mode="wb", lazy=False), required=False)
@cli_flag(
    "-m",
    "--merge",
    help="Merge subsequent SGRs into single pieces instead of processing the one-by-one. "
    "Useful when there is a necessity to inspect any other types of sequences, such "
    "as cursor controlling or display erasing ones.",
)
@cli_option(
    "-d",
    "--delay",
    type=FloatRange(_min=1e-9, max_open=True),
    default=0.4,
    show_default=True,
    metavar="SECONDS",
    help="Floating-point value determining the interval between processing each of split "
    "data chunks. This option takes effect only in automatic mode and is silently "
    "ignored in manual mode.",
)
def invoker(**kwargs):
    """
    {{Send mode}}

    Open specified INFILE in binary mode and start reading the content to the buffer.
    If omitted or specified as ''-'', the stdin will be used as data input instead.
    Split the data by ESC control bytes (`0x1b`) and feed the parts one-by-one to
    OUTFILE, or to a "prepared named pipe" in a system temporary directory, if no
    OUTFILE is specified. Manual control is available only if stdin of the
    process is a terminal, otherwise the automatic data writing is performed.\n\n

    {{Receive mode}}

    Open specified INFILE in binary mode, start reading the content and immediately
    write the results to stdout. If INFILE is omitted, read from the same named pipe
    as in send mode instead (the filename is always the same). Second argument is
    ignored. No stream control is implemented. Terminate on EOF.\n\n

    {{Statusbar}}

    Status example:\n\n

    ` <stdin> → /tmp/es7s-esqdb-pipe   F P A M                 4+37     12/32440`
    """
    from es7s.cmd.esqdb import action

    action(**kwargs)
