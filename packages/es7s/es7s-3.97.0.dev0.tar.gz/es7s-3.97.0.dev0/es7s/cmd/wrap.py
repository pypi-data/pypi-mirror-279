# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from pathlib import Path

import pytermor as pt

from es7s.shared import get_stdout, get_demo_res
from ._adaptive_input import _AdaptiveInputAction
from ._base import _BaseAction


class action(_AdaptiveInputAction, _BaseAction):
    PRIVATE_REPLACER = "\U000E5750"

    def __init__(self, force_width: int = None, max_width: int = None, **kwargs):
        super().__init__(**kwargs)

        if force_width is not None:
            width = force_width
        else:
            width = pt.get_terminal_width(pad=0)
            if max_width:
                width = min(max_width, width)

        self._run(width)

    def _get_demo_input(self) -> Path | None:
        return get_demo_res("demo-wrap.txt")

    def _run(self, width: int):
        result = pt.wrap_sgr(self._input_lines, width)
        get_stdout().echo(result)
