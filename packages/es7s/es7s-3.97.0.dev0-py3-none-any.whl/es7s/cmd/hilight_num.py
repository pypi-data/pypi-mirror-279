# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re
import typing as t
from pathlib import Path

import pytermor as pt

from es7s.shared import get_stdout
from es7s.shared import get_demo_res
from ._adaptive_input import _AdaptiveInputAction
from ._base import _BaseAction


class WhitespaceBytesSquasher(pt.IFilter[bytes, bytes]):
    def __init__(self):
        super().__init__()
        self._pattern = re.compile(rb"\s+")
        self._repl = lambda m: b"." * len(m.group())

    def _apply(self, inp: bytes, extra: t.Any = None) -> bytes:
        return self._pattern.sub(self._repl, inp)


class action(_AdaptiveInputAction, _BaseAction):
    CHUNK_SIZE = 1024

    RAW_FILTERS = [
        pt.OmniSanitizer(b"."),
        WhitespaceBytesSquasher(),
    ]

    _RGB_COLOR_REGEX = re.compile(
        r"""
        (
        (\#?(([0-9a-f])\4\4))
        | 
        ((?:\#|0x)?([0-9a-f]{6})) 
        )
        """,
        flags=re.IGNORECASE | re.VERBOSE,
    )

    def __init__(self, **kwargs):
        self._line_num = 1
        self._offset = 0
        super().__init__(**kwargs)

        self._run()

    def _get_demo_input(self) -> Path:
        return get_demo_res("demo-hilight.txt")

    def _run(self):
        for line in self._input_lines:
            processed_line = self._process_decoded_line(line)
            get_stdout().echo(processed_line)

    def _process_decoded_line(self, line: str | None) -> str:
        if line is None:
            return ""
        line_len = len(line.encode())
        result = pt.highlight(line.strip("\n"))

        self._line_num += 1
        self._offset += line_len
        return get_stdout().render(result)
