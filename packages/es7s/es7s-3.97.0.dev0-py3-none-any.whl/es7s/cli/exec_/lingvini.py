# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from .._decorators import catch_and_log_and_exit, cli_argument, cli_command, cli_flag


@cli_command(__file__, "programming language statistics")
@cli_argument("path", type=click.Path(exists=True), nargs=-1, required=False)
@cli_flag("-D", "--docker", help="Run github-linguist in a docker container.")
@cli_flag(
    "-N",
    "--no-cache",
    help="Calculate the value regardless of the cache state and do not update it.",
)
@cli_flag("-l", "--list", help="List the languages and colors and exit.")
@catch_and_log_and_exit
def invoker(*args, **kwargs):
    """
    Requires ++github-linguist++ executable to be installed and available in
    PATH, or ++github-linguist++ docker image to be available (when '-D' is in use):
    https://github.com/github-linguist/linguist
    """
    from es7s.cmd.lingvini import action

    action(*args, **kwargs)
