# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from pathlib import Path

import click

from .._base_opts_params import CMDTRAIT_X11
from .._decorators import catch_and_log_and_exit, cli_command, cli_argument


@cli_command(
    __file__,
    "open terminal in a specified working directory",
    traits=[CMDTRAIT_X11],
    ignore_unknown_options=True,
    allow_extra_args=True,
)
@cli_argument(
    "workdir", type=click.Path(exists=True, resolve_path=True, path_type=Path), default="."
)
@cli_argument(
    "args",
    nargs=-1,
    required=False,
)
@catch_and_log_and_exit
def invoker(*args, **kwargs):
    """
    Open terminal in a working directory specified with WORKDIR, which can be a
    path to a directory, or to a file as well (in latter case working directory
    will be a parent dir of that file). If WORKDIR is omitted, current working
    directory will be used.
    """
    from es7s.cmd.open_terminal import action

    action(*args, **kwargs)
