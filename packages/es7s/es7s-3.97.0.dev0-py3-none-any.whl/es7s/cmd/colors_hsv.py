# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import io
import typing

import pytermor as pt

from es7s.shared import make_interceptor_io
from ._base import _BaseAction

_T = typing.TypeVar("_T")


class action(_BaseAction):

    H_VALUES = [*range(0, 360, 10)]
    # S_VALUES = [*range(0, 110, 10)]
    S_VALUES = [15, 30, 40, 56, 100]
    # V_VALUES = [*range(0, 110, 10)]
    V_VALUES = [30, 50, 70, 85, 100]

    XTERM_16_VALUES = [
        [*range(0, 8)],
        [*range(8, 16)],
    ]
    GRAYSCALE_VALUES = [16, *range(232, 256), 231]

    H_FMT = pt.Style(fg=pt.cv.GRAY_30, overlined=True)
    S_FMT = pt.Style(fg=pt.cv.GRAY_93, bg=pt.cv.GRAY_0)

    V_FMT = pt.Style(fg=pt.cv.GRAY_30)
    A_FMT = pt.Style(fg=pt.cv.GRAY_70, bold=True)

    def __init__(self, compact: bool, **kwargs):
        self._compact_mode = pt.get_terminal_width(pad=0) < 200
        if compact is not None:
            self._compact_mode = compact
        self._out = make_interceptor_io(io.StringIO())
        self._CELL_WIDTH = [5, 3][self._compact_mode]

        self._last_cell_code: int | None = None
        self._run()
        self._out.flush_buffer()

    def _mds(self, default: _T, compact: _T) -> _T:
        return compact if self._compact_mode else default

    def _becho_rendered(self, *args, nl=True):
        self._out.echo_rendered(*args, nl=nl)
        if nl:
            self._out.flush_buffer()

    def _format_col_label(self, h: int) -> str:
        return (f"{h:3d}" + self._mds("°", "") if h % 30 == 0 else "").center(self._CELL_WIDTH)

    def _format_row_label(self, v: int | None, sep: str = "│") -> str:
        result = ""
        if isinstance(v, int):
            result = self._mds(f"{v}% ", f"{v:>3d}")
        return self._mds(" ", "") + result.rjust(self._CELL_WIDTH) + sep

    def _get_border_fmt(self, s: int, v: int) -> pt.Style:
        return self.H_FMT if (v == self.V_VALUES[0] and s > self.S_VALUES[0]) else self.V_FMT

    def _print_row_label(self, s: int, v: int | None):
        self._becho_rendered(self._format_row_label(v), self._get_border_fmt(s, v), nl=False)

    def _print_row_label_right(self, s: int, v: int):
        self._becho_rendered(
            self._format_row_label(s if v == self.V_VALUES[len(self.V_VALUES) // 2] else None),
            self._get_border_fmt(s, v),
        )

    def _print_table_header(self, s: int):
        self._print_attribute(*self._mds(("  V", "↓  "), ("V%", "↓")))
        self._print_vert_sep()
        for idx, h in enumerate(self.H_VALUES):
            if h == self.H_VALUES[len(self.H_VALUES) // 2]:
                self._print_attribute(*self._mds(("← H", " →"), ("↔H", "°")))
            else:
                self._becho_rendered(self._format_col_label(h), self.V_FMT, nl=False)
        self._print_vert_sep()
        self._print_attribute(*self._mds(("  S", "↓  "), ("S%", "↓")))
        self._print_vert_sep()
        self._out.echo()

    def _print_attribute(self, name: str, arrow: str):
        self._becho_rendered(f"{name}{arrow}", self.A_FMT, nl=False)

    def _print_vert_sep(
        self,
    ):
        self._becho_rendered("│", self.V_FMT, nl=False)

    def _print_horiz_sep(self, sep, hidden=False, double=False, over=False, label=None):
        sep = (
            self._format_row_label(None, sep=sep)
            + "".ljust(len(self.H_VALUES) * self._CELL_WIDTH)
            + sep
            + self._format_row_label(None, sep=sep)
        )
        if label:
            sep = sep[: sep.rindex(" " * len(label))] + label
        st = self.V_FMT
        if over:
            st = pt.Style(st, overlined=True)
        if hidden:
            return self._becho_rendered(sep.replace(" ", " "), st)
        if double:
            return self._becho_rendered(sep.replace(" ", "═"), st)
        return self._becho_rendered(sep.replace(" ", "─"), st)

    def _print_cell(self, h: int, s: int, v: int, code: int = None, width_override: int = None):
        col = None
        if code is None:
            approx = pt.approximate(pt.HSV(h, s / 100, v / 100), pt.Color256, max_results=5)
            cols = [c for c in approx if not c.color._color16_equiv]
            if not cols:
                self._becho_rendered("".ljust(self._CELL_WIDTH), nl=False)
                return
            col = cols[0].color
            code = col.code
        if not col:
            col = pt.Color256.get_by_code(code)

        label_val = ""
        if col.code != self._last_cell_code:
            label_val = self._mds("▏", "") + f"{col.code:3d}" + self._mds(" ", "")
        self._last_cell_code = col.code
        self._becho_rendered(
            label_val.center(width_override or self._CELL_WIDTH),
            pt.Style(bg=col, overlined=True).autopick_fg(),
            nl=False,
        )

    def _run(self):
        self._print_horiz_sep("╷")
        self._print_table_header(0)
        self._print_horiz_sep("│")

        for s in self.S_VALUES:
            for v in self.V_VALUES:
                self._print_row_label(s, v)
                self._last_cell_code = None
                for h in self.H_VALUES:
                    self._print_cell(h, s, v)
                self._becho_rendered("│", self.V_FMT, nl=False)
                self._print_row_label_right(s, v)

        self._print_horiz_sep("│", hidden=True, over=True)

        for cidx, cc in enumerate(self.XTERM_16_VALUES):
            self._print_row_label(0, None)
            self._becho_rendered(pt.pad(self._mds(2, 0)), nl=False)
            for c in cc:
                self._print_cell(0, 0, 0, code=c, width_override=5)

            self._becho_rendered(pt.pad(self._mds(6, 3)), nl=False)
            for gidx, c in enumerate(self.GRAYSCALE_VALUES):
                if self._compact_mode:
                    if (cidx == 0) != (gidx < len(self.GRAYSCALE_VALUES) // 2):
                        continue
                else:
                    if cidx == 1:
                        self._becho_rendered(pt.pad(self._CELL_WIDTH), nl=False)
                        continue
                self._print_cell(0, 0, 0, code=c, width_override=5)
            self._becho_rendered(pt.pad(self._mds(2, 0)), nl=False)
            self._becho_rendered("│", self.V_FMT, nl=False)
            self._print_row_label_right(0, 0)

        self._print_horiz_sep("│", hidden=True)
        self._print_horiz_sep(
            " ",
            hidden=True,
            over=True,
            label="["
            + self._mds("Widescreen mode", f"Compact mode: W={pt.get_terminal_width(pad=0)} < 200")
            + "]",
        )
