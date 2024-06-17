# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from es7s.cli._base_opts_params import CMDTRAIT_ADAPTIVE_OUTPUT, EnumChoice, HelpPart
from es7s.cli._decorators import cli_argument
from es7s.shared.enum import PrintFfmpegMode
from ..._decorators import catch_and_log_and_exit, cli_command


@cli_command(
    __file__,
    "print ffmpeg codecs list",
    traits=[CMDTRAIT_ADAPTIVE_OUTPUT],
    interlog=[
        HelpPart(
            "MODE should be one of: " + ", ".join(f"*{v}*" for v in PrintFfmpegMode.list()) + "."
        ),
    ],
)
@cli_argument(
    "mode", type=EnumChoice(PrintFfmpegMode), required=True, default=PrintFfmpegMode.CODECS
)
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Print formatted list of ++ffmpeg++ decoders/encoders/both, which must
    be available. Expected formatting as of 'ffmpeg' version 4.2.7. The
    output is @A> adjusted depending on a terminal size.
    """
    from es7s.cmd.print_ffmpeg_codecs import action

    action(**kwargs)
