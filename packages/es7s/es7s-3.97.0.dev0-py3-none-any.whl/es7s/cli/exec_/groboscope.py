3  # ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from es7s.cli._decorators import cli_adaptive_input, AdaptiveInputAttrs, cli_flag
from .._base_opts_params import CMDTRAIT_ADAPTIVE_INPUT
from .._decorators import cli_command, catch_and_log_and_exit


@cli_command(
    __file__,
    "&(gro)up &brutef&orce &d&eco&der",
    traits=[CMDTRAIT_ADAPTIVE_INPUT],
    **AdaptiveInputAttrs,
)
@cli_adaptive_input(demo=True)
@cli_flag(
    "-s", "--stats", help="Display character frequency table for all code page pairs and exit."
)
@cli_flag("-b", "--build", help="Rebuild frequency tables and exit.")
@cli_flag(
    "-f",
    "--full",
    help="Do not truncate the results. This option also makes the results to go to stdout.",
)
@cli_flag("-o", "--one", help="{{@TODO pick best match (heuristics?)}}")
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Read the data (see below) and analyze code point frequency distribution.
    Intended usage is to suggest the interpreted and the actual encoding of
    the corrupted data, i.e. the codepage that was used to decode the data, as
    well as the codepage that was used to ENCODE the original data. Then
    sort the list of code page pairs (most matching first), and attempt to
    perform an inverse operation of encoding and decoding for each. The
    operation with highest cyrillic code point ratio is implied to be the
    result.\n\n

    The command
    works for cyrillic pre-UTF-8 encodings: *KOI8-R*, *CP-886*, *CP-437*,
    *Windows-1251*, *Windows-1252*, *ISO-8559-5*, *Macintosh*, and *UTF-8*
    itself.
    """
    from es7s.cmd.groboscope import action

    if kwargs.get("build"):
        kwargs.update({"demo": True})
    if kwargs.get("stats"):
        kwargs.update({"input": "\n"})
    action(**kwargs)
