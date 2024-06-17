# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import importlib

from .._base_opts_params import IntRange, CMDTYPE_BUILTIN, CMDTRAIT_ADAPTIVE_OUTPUT
from .._decorators import (
    catch_and_log_and_exit,
    cli_command,
    cli_multithreaded,
    cli_flag,
    cli_adaptive_input,
    AdaptiveInputAttrs,
)
from ... import APP_NAME

_ACTION_MODULE = f"{APP_NAME}.cmd.transmorph"


@cli_command(
    __file__,
    import_from=_ACTION_MODULE,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE_OUTPUT],
    short_help="rephrase input text preserving the semantics",
    # epilog=[HelpPart("Result", title="Result filtering:")],
    **AdaptiveInputAttrs,
)
@cli_adaptive_input()
@cli_multithreaded()
@cli_flag("-a", "--all", help="Query all languages, not only ones from the preset list (slow).")
@cli_flag("-f", "--full", help="Display all query results instead of a few ones.")
@cli_flag("-M", "--porcelain", help="Produce machine-readable output to stdout.")
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Rephrase specified INPUT text preserving the semantics (more or less).\n\n

    Under the hood queries translations API and perform double translation from
    ORIGIN language to each one in the preset list and then from the currently
    processed language back to ORIGIN. ORIGIN language can be customized with
    <general.default-lang-code> config option, while preset list is defined as
    <~preset-lang-codes> option.\n\n

    In addition to INPUT specified via arguments, the app can read it from the file(s),
    which names should be provided with '-F' option(s); use '-F -' or '-S' to
    specify standard input stream. Text is split by newlines; note that two
    consecutive empty lines are treated as EOF and the reading from that file stops.\n\n

    Write the results into standard output stream; progress bar and separators are
    printed into standard error stream instead. If stdout is a terminal, each result
    is prefixed with extra info (language code and \\"distance\\" from the origin).\n\n

    '-T0' instructs the program to use optimal number of threads equal to number
    of logical CPU cores × 2. This can be limited by <~auto-threads-limit>
    config option.\n\n

    Machine-readable output can be enabled with '-M', format is:\n\n

         `OUTPUT`   =  {{GROUP_1}} *GS* {{GROUP_2}} *GS* ... *GS*\n
         [GROUP]    =  {RESULT_1} *RS* {RESULT_2} *RS* ... *RS*\n
        {RESULT}  = (UTF-8 string)\n\n

    where <GS> is 0x1E GROUP SEPARATOR, and <RS> is 0x1D RECORD SEPARATOR.

    Powered by ++Yandex.Cloud++.\n
    """
    getattr(importlib.import_module(_ACTION_MODULE), "action")(**kwargs)
