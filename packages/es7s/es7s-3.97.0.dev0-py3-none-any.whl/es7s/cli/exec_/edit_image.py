# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from .._base_opts_params import CMDTRAIT_X11
from .._decorators import catch_and_log_and_exit, cli_command, cli_argument


@cli_command(__file__, "open image in a graph editor", traits=[CMDTRAIT_X11])
@cli_argument("file", type=click.Path(exists=True, dir_okay=False))
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Open an image file specified with FILE in a graphic editor. Editors can be
    configured with <.editor-raster> and <.editor-vector> config variables defined
    in <cmd.edit-image> section. The type of an image is determined by comparing
    its extension with <.ext-vector> list from the same config section.
    """
    from es7s.cmd.edit_image import action
    action(**kwargs)
