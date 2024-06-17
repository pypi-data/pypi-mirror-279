# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023-2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re

import pytermor as pt

from es7s.shared import (
    get_dist_uconfig,
    get_merged_uconfig,
    get_stdout,
    FrozenStyle,
    get_logger,
    Styles as BaseStyles,
)
from ._base import _BaseAction


class _Styles(BaseStyles):
    def __init__(self):
        self.SECTION = FrozenStyle(fg=pt.cv.YELLOW)
        self.OPT_NAME = FrozenStyle(fg=pt.cv.BLUE)
        self.OPT_VALUE = FrozenStyle(fg=pt.cv.GREEN)
        self.OPT_DEFAULT_NAME = FrozenStyle(fg=pt.cv.GRAY_50)
        self.OPT_DEFAULT_VALUE = FrozenStyle()


class action_list(_BaseAction):
    def __init__(self, *args, **kwargs):
        self._styles = _Styles()
        self._run()

    def _run(self):
        config = get_merged_uconfig()
        dist_config = get_dist_uconfig()
        stdout = get_stdout()
        warnings = []

        for idx, sec_name in enumerate(sorted(config.sections())):
            if idx > 0:
                stdout.echo()
            stdout.echo_rendered(f"[{sec_name}]", self._styles.SECTION)

            section = config.get_section(sec_name)
            dist_section = None
            try:
                dist_section = dist_config.get_section(sec_name)
            except ValueError:
                warnings.append(
                    "User config contains probably deprecated section "
                    f"{sec_name!r} (missing in dist config)"
                )

            for opt_name in config.options(sec_name):
                opt_st = self._styles.OPT_NAME
                val_st = self._styles.OPT_VALUE
                value = section.get(opt_name)

                if dist_section:
                    defvalue = dist_section.get(opt_name, fallback=None)
                    if defvalue is not None and value == defvalue:
                        opt_st = self._styles.OPT_DEFAULT_NAME
                        val_st = self._styles.OPT_DEFAULT_VALUE
                option_fmtd = stdout.render(opt_name + " = ", opt_st)
                value_fmtd = self._render_value(value, val_st)
                stdout.echo_rendered(option_fmtd + value_fmtd)

        for warning in warnings:
            get_logger().warning(warning)

    def _render_value(self, val: str, val_st: pt.Style) -> str:
        val = re.sub("\n+", "\n    ", val)
        return get_stdout().render(val, val_st)
