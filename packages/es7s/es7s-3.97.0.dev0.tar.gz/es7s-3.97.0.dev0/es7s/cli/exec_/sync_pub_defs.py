# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from pathlib import Path

import click

from .._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_NONE
from .._decorators import cli_command, cli_argument, cli_option, catch_and_log_and_exit


@cli_command(
    name=__file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_NONE],
    short_help="find all public defs and compose an import __init__ file",
)
@cli_argument(
    "target",
    type=click.Path(exists=True, file_okay=False, writable=True, resolve_path=True, path_type=Path),
    required=True,
    nargs=-1,
)
@cli_option(
    "-u",
    "--update",
    is_flag=True,
    help="Update __init__.py file in each TARGET's root folder, make a copy of the original file beforehands.",
)
@cli_option(
    "-B",
    "--no-backup",
    is_flag=True,
    help="Do not make a copy of the original __init__.py (implies '-u').",
)
@catch_and_log_and_exit
def invoker(*args, **kwargs):
    """
    Find all Python files in TARGET folder and subfolders, and compose an import
    __init__ file contents out of all public definitions found. Print the
    contents to stdout or replace the original __init__.py file with '-u'.\n\n

    If update mode is enabled, also merge the imports from the original file
    with generated ones, skipping aliased imports (i.e. keep them untouched).
    Note that in this mode the final imports are unsorted -- first there are
    original imports from the existing file, and then new ones are added (the
    ones that are missing).
    """
    from es7s.cmd.sync_pub_defs import action

    action(*args, **kwargs)
