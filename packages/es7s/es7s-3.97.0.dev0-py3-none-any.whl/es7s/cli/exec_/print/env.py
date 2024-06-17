# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

from es7s.cli._decorators import cli_adaptive_input
from es7s.shared.enum import MarginMode, QuoteMode
from ..._base import CliCommand
from ..._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_ADAPTIVE_OUTPUT, EnumChoice, HelpPart
from ..._decorators import cli_argument, cli_command, catch_and_log_and_exit, cli_option


@cli_command(
    name=__file__,
    cls=CliCommand,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE_OUTPUT],
    short_help="system/stdin env variables",
    interlog=[
        HelpPart(
            "There is a support for result filtering; by default FILTERs are treated as extended regular "
            "expressions, but this can be altered with '--literal' option. Considerations:",
            "Filters:",
        ),
        HelpPart(
            "⏺ When there are two or more FILTERs specified, a key is considered matching if *any* of these "
            "filters do (i.e. OR operand is applied). Use '--and' to change this behaviour: with the option the "
            "variable will be printed only if *all* filters consequently match the var name.",
            indent_shift=1,
        ),
        HelpPart(
            "⏺ Search is case-insensitive unless any of filters contain one or more capital letters, in which "
            "case the search will be case-sensitive (however, this does not apply to literal mode, which is "
            "always case-sensitive).",
            indent_shift=1,
        ),
    ],
    command_examples=[
        "1. read from system environment, filter by string:",
        "     {} --literal term",
        "2. read from system environment, filter by regexps (OR):",
        "     {} ^term ssh",
        "3. read from a file, filter by regexps (AND):",
        "     {} -F .env --and ^term ssh",
        "4. read from stdin, split by NUL byte:",
        "     {} -S -0",
    ],
)
@cli_adaptive_input(input_args=False, null=True, default_stdin=False)
@cli_argument("filter", nargs=-1, required=False)
@cli_option(
    "-l",
    "--literal",
    is_flag=True,
    default=False,
    help="Treat specified FILTERs as plain strings [default: as extended regexps].",
)
@cli_option(
    "-a",
    "--and",
    is_flag=True,
    default=False,
    help="Require *all* specified FILTERs to match the variable key [default: any FILTER].",
)
@cli_option(
    "-m",
    "--margin",
    type=EnumChoice(MarginMode, inline_choices=True),
    default=MarginMode.FULL,
    show_default=True,
    metavar="SIZE",
    help="Horizontal space around the output:",
)
@cli_option(
    "-q",
    "--quote",
    type=EnumChoice(QuoteMode, inline_choices=True),
    default=QuoteMode.AUTO,
    show_default=True,
    metavar="WHEN",
    help="Wrap values in quotes:",
)
@cli_option(
    "-n",
    "--no-prefix",
    is_flag=True,
    default=False,
    help="Do not prepend variable names with context-dependant prefixes.",
)
@cli_option(
    "-k",
    "--keep-sgr",
    is_flag=True,
    default=False,
    help="Do not remove SGRs from values even when '--no-color' is active.",
)
@catch_and_log_and_exit
class invoker:
    """
    One more environment variable list pretty-printer. Default mode: run '/bin/env',
    format its output and print the result. '-S' flag switches the application
    to reading and formatting standard input instead.\n\n

    Supports pretty-printing of various application configs including 'mc',
    'git' or 'php', as well as any other configuration file which follows this
    syntax (spaces around ''='' can be omitted; quotes are required only for
    values containing whitespace; key-value pairs are separated with 0x0A LINE
    FEED):\n\n

        `key = ""value""`\n\n

    This command requires ++/bin/env++ to be present and available.\n\n
    """

    def __init__(self, **kwargs):
        from es7s.cmd.print_env import action

        action(**kwargs)
