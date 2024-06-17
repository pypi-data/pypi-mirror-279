# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from collections.abc import Iterable
from pathlib import Path

from es7s.shared import run_subprocess
from es7s.shared.path import TERMINAL_EXECUTABLE
from ._base import _BaseAction


class action(_BaseAction):
    def __init__(self, *args, **kwargs):
        self._run(*args, **kwargs)

    def _run(self, workdir: Path, args: Iterable[str]):
        if not workdir.is_dir():
            workdir = workdir.parent
        run_subprocess(TERMINAL_EXECUTABLE, "--working-directory", workdir, *args)
