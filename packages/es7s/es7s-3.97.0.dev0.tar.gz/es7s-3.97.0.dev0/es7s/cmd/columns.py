# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from pathlib import Path

from es7s_commons import columns

from es7s.shared import get_stdout, get_demo_res, get_logger
from ._adaptive_input import _AdaptiveInputAction
from ._base import _BaseAction


class action(_AdaptiveInputAction, _BaseAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        del kwargs["file"], kwargs["stdin"], kwargs["demo"]
        self._run(**kwargs)

    def _get_demo_input(self) -> Path | None:
        return get_demo_res("demo-columns.txt")

    def _run(self, **kwargs):
        result, ts = columns(self._input_lines, **kwargs)
        get_stdout().echo(result)
        get_logger().debug(ts)
