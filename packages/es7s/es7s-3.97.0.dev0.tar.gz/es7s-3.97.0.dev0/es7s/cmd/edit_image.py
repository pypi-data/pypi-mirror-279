# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os.path

import click

from es7s.shared import get_logger, run_subprocess
from ._base import _BaseAction


class action(_BaseAction):
    def __init__(self, **kwargs):
        self._run(**kwargs)

    def _run(self, file: click.Path):
        _, ext = os.path.splitext(str(file))
        ext_vector: list[str] = self.uconfig().get("ext-vector", list, str)
        editor_type = "raster"
        if ext.removeprefix(".") in ext_vector:
            editor_type = "vector"
        get_logger().debug(f"Selected editor type: {editor_type}")

        editor = self.uconfig().get(f"editor-{editor_type}")
        run_subprocess(editor, file)
