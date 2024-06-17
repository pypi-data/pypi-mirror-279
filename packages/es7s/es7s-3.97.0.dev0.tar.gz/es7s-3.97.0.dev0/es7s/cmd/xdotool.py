# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re
from collections.abc import Iterator

from es7s.shared import get_user_data_dir, run_subprocess
from es7s.shared.path import XDOTOOL_PATH
from ._base import _BaseAction


class action(_BaseAction):
    PRESET_SLEEP_INTERVAL = 0.25

    def __init__(self, literal: bool, timeout: float, **kwargs):
        self._literal = literal
        self._timeout: float|None = timeout or None
        self._run([*kwargs.pop('args')])

    def _run(self, args: list[str]):
        cmd = [XDOTOOL_PATH]
        if self._literal:
            cmd.extend(args)
        else:
            while args:
                filename = args.pop(0)
                cmd.extend(self._read_preset(filename))
                if len(args):
                    cmd.extend(['sleep', str(self.PRESET_SLEEP_INTERVAL)])
        run_subprocess(*cmd, timeout=self._timeout)

    def _read_preset(self, filename: str) -> Iterator[str]:
        path = None
        for fname in (filename, f"{filename}.xdo"):
            path = get_user_data_dir() / "xdotool" / fname
            if not path.is_file():
                continue
            with open(path, 'rt') as f:
                for line in f.readlines():
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    yield from re.split(r'\s+', line)
                break
        else:
            raise FileNotFoundError(path or filename)
