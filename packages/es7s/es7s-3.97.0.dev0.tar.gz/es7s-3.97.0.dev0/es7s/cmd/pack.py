# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import shutil
from pathlib import Path
from typing import Iterable

from ._base import _BaseAction


class _action_pack(_BaseAction):
    FORMATS = ["zip", "rar", "gzip", "tar", "7z"]
    EXECUTABLES = {}

    def _find_executables(self):
        for fmt in self.FORMATS:
            if path := shutil.which(fmt):
                self.EXECUTABLES[fmt] = path

    def _get_archiver(self, fmt: str) -> str | None:
        if len(self.EXECUTABLES) == 0:
            self._find_executables()
        return self.EXECUTABLES.get(fmt, None)


class action_pet(_action_pack):
    def __init__(self, file: Iterable[Path], **kwargs):
        self._files = [*file]
        self._run()

    def _run(self):
        print(self._files)
        [print(self._get_archiver(fmt)) for fmt in self.FORMATS]


class action_pup(_action_pack):
    def __init__(
        self,
        archive: Path,
        file: Iterable[Path],
        add: bool,
        move: bool,
        extract: bool,
        list: bool,
        **kwargs,
    ):
        self._archive = archive
        self._files = [*file]
        self._run()

    def _run(self):
        print(self._files)
        [print(self._get_archiver(fmt)) for fmt in self.FORMATS]
