# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from .._base_opts_params import IntRange
from .._decorators import cli_command, cli_argument, cli_option, catch_and_log_and_exit


@cli_command(__file__, "extract emojis from emoji font to png files")
@cli_argument(
    "char",
    type=str,
    required=False,
    nargs=-1,
)
@cli_option(
    "-s",
    "--size",
    default=128,
    show_default=True,
    type=IntRange(1, max_open=True),
    help="Output image(s) width and height (which are equal).",
)
@cli_option(
    "-f",
    "--font",
    default="Noto Color Emoji",
    show_default=True,
    help="Font name to use for rendering.",
)
@cli_option(
    "-o",
    "--output",
    default="emoji-%s",
    show_default=True,
    help='Output filename template, must contain ""%s"".',
)
@catch_and_log_and_exit
def invoker(*args, **kwargs):
    """
    Extract emojis from an emoji font to separate PNG files.
    """
    from es7s.cmd.render_emoji import action

    action(*args, **kwargs)
