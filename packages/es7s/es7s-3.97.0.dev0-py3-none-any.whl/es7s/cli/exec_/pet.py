# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from pathlib import Path

import click

from ...cli._base_opts_params import CMDTYPE_DRAFT, CMDTRAIT_NONE
from ...cli._decorators import cli_command, cli_argument, catch_and_log_and_exit


@cli_command(__file__, "&pack &efficiency &test", type=CMDTYPE_DRAFT, traits=[CMDTRAIT_NONE])
@cli_argument(
    "file",
    type=click.Path(allow_dash=True, resolve_path=True, path_type=Path),
    required=True,
    nargs=-1,
)
@catch_and_log_and_exit
def invoker(*args, **kwargs):
    """
    @TODO display compress rate for a given file using a set of various archivers
    """
    from es7s.cmd.pack import action_pet as action

    action(*args, **kwargs)
