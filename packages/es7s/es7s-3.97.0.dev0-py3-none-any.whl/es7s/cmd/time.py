# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import time
import typing
from collections.abc import Iterable
from datetime import datetime
from functools import lru_cache
from math import floor

import pytermor as pt
from es7s_commons import to_superscript

from ._base import _BaseAction
from ._full_terminal import _FullTerminalAction, Message, CycledChoice, Toggle, CycledCounter
from ..shared import ThemeColor, get_logger


class action(_FullTerminalAction, _BaseAction):
    _CHAR_FILLED = "░▒▓█"
    _CHAR_EMPTY = " "
    _ZOOM_MAX = 10

    def __init__(
        self,
        format: str,
        seconds: bool,
        debug: bool,
        intensity: int,
        narrow: bool,
        text_color: str,
        **kwargs,
    ):
        if seconds:
            format = "%T"

        super().__init__(**kwargs)

        formats = ["%R", "%T"]
        if format not in formats:
            formats = [format, *formats]

        self._format = self._bind("format", CycledChoice[str](formats))
        self._intensity = self._bind(
            "intensity", CycledChoice[str]([*self._CHAR_FILLED], init_idx=(intensity - 1))
        )
        self._zoom = self._bind("zoom", CycledCounter(self._ZOOM_MAX, 1, self._ZOOM_MAX, -1))
        self._double_width = self._bind("wide/narrow", Toggle(init=not narrow))

        initial_color = ThemeColor()
        try:
            initial_color = pt.resolve_color(text_color)
        except LookupError:
            pass
        self._text_color = self._bind(
            "textcolor",
            CycledChoice[pt.Color](
                [pt.Color16.get_by_code(cc) for cc in range(31, 38)],
                init=initial_color,
            ),
            callback=self._update_style,
        )
        self._debug = self._bind("debug", Toggle(init=debug), key="D")

        self._update_style()
        self._run()

    def _update_style(self):
        self._text_st = pt.FrozenStyle(fg=self._text_color.current)

    def _run(self):
        self._main_loop()

    def _render(self):
        dt = datetime.fromtimestamp(time.time_ns() / 1e9)
        dtstr = dt.strftime(self._format.current)

        chars = []
        for s in dtstr or "°":
            if chars:
                chars.append(C_SEP)
            chars.append(self._get_char(s.upper()))
        nominal_w = sum(map(len, chars))

        coef_w = (1, 2)[self._double_width.current]
        scale_ratio = min(
            max(1, floor(self._term_width / (nominal_w * coef_w))),
            max(1, floor(self._term_height / CharMap.NOMINAL_HEIGHT)),
        )
        scale_limit = self._zoom.current
        if 0 < scale_limit < scale_ratio:
            scale_ratio = scale_limit
        else:
            self._zoom.set(scale_ratio)

        actual_w = nominal_w * scale_ratio * coef_w
        actual_h = CharMap.NOMINAL_HEIGHT * scale_ratio
        margin_x = self._term_width - actual_w
        margin_y = self._term_height - actual_h
        margin_left = margin_x // 2
        margin_top = margin_y // 2

        srcs = [C.generator() for C in chars]
        lines: list[str] = []
        for src_idx in range(CharMap.NOMINAL_HEIGHT):
            line = ""
            for src in srcs:
                if src:
                    chline: str = next(src)
                    linept = ""
                    for cpart in chline:
                        if not self._debug.current:
                            linept += cpart * scale_ratio * coef_w
                        else:
                            linept += cpart + (((scale_ratio * coef_w) - 1) * "_")
                    line += linept
            lines.extend([line] * scale_ratio)

        for (ln_idx, ln) in enumerate(lines):
            self._set_cursor(margin_top + ln_idx + 1, margin_left + 1)
            ln_pp = ln.translate(self._get_trans_table(self._intensity.current))
            self._interceptor.echo_rendered(ln_pp[: self._term_width], self._text_st)

    def _get_char(self, s: str) -> "Char":
        chars = CHARS_DEBUG if self._debug.current else CHARS
        return chars.get(s, C_UNDEF(s))

    @lru_cache
    def _get_trans_table(self, char_filled: str) -> dict[int, str]:
        return {
            ord("@"): char_filled,
            ord("."): self._CHAR_EMPTY,
        }

    def _custom_keypress(self, key: str):
        if self._debug.current:
            self._messages.clear()

        super()._custom_keypress(key)

        if self._debug.current:
            self._messages.append(
                Message(
                    "[DEBUG] "
                    + "  ".join(f"{kl.key}={kl.var.current}" for kl in self._key_listeners),
                    None,
                ),
            )

    def _on_terminal_resize(self):
        self._zoom.set(0)


class CharMap:
    MAX_WIDTH = 5
    NOMINAL_HEIGHT = 5

    # fmt: off
    _DATA = (
        "  .   .@.  @.@  @.@  .@@  @.@  .@@.  @   .@    @.  @.@  ...  ..   ...   .   ..@ "  # 
        "  .   .@.  @.@  @@@  @@.  ..@  @..@  @   @.    .@  .@.  .@.  ..   ...   .   ..@ "  # 
        "  .   .@.  ...  @.@  .@.  .@.  .@..  .   @.    .@  @.@  @@@  ..   @@@   .   .@. "  # 2x
        "  .   ...  ...  @@@  .@@  @..  @.@.  .   @.    .@  ...  .@.  .@   ...   .   @.. "  # 
        "  .   .@.  ...  @.@  @@.  @.@  @@.@  .   .@    @.  ...  ...  @.   ...   @   @.. "  # 
                                                                                           
        " .@.  .@.  @@.  @@.  ..@  @@@  .@@  @@@  .@.  .@.   .   ...  ..@  ...  @..  @@. "  # 
        " @.@  @@.  ..@  ..@  .@@  @..  @..  ..@  @.@  @.@   @   .@.  .@.  @@@  .@.  ..@ "  # 
        " @.@  .@.  .@@  .@.  @.@  @@.  @@.  .@.  .@.  .@@   .   ...  @..  ...  ..@  .@. "  # 3x
        " @.@  .@.  @..  ..@  @@@  ..@  @.@  .@.  @.@  ..@   @   .@.  .@.  @@@  .@.  ... "  # 
        " .@.  @@@  @@@  @@.  ..@  @@.  .@.  @..  .@.  @@.   .   @..  ..@  ...  @..  .@. "  # 
                                                                                           
        " .@@. .@.  @@.  .@@  @@.  @@@  @@@  .@@  @.@  .@.  ..@  @.@  @.. @...@ @@.  .@. "  # 
        " @..@ @.@  @.@  @..  @.@  @..  @..  @..  @.@  .@.  ..@  @@.  @.. @@.@@ @.@  @.@ "  # 
        " @.@@ @@@  @@.  @..  @.@  @@.  @@.  @.@  @@@  .@.  @.@  @..  @.. @.@.@ @.@  @.@ "  # 4x
        " @... @.@  @.@  @..  @.@  @..  @..  @.@  @.@  .@.  @.@  @@.  @.. @...@ @.@  @.@ "  # 
        " .@@@ @.@  @@.  .@@  @@.  @@@  @..  .@@  @.@  .@.  .@.  @.@  @@@ @...@ @.@  .@. "  # 
                                                                                           
        " @@.  .@.  @@.  .@@  @@@  @.@  @.@ @...@ @.@  @.@  @@@  @@@  @..  @@@  .@.  ... "  # 
        " @.@  @.@  @.@  @..  .@.  @.@  @.@ @...@ @.@  @.@  ..@  @..  @..  ..@  @.@  ... "  # 
        " @@.  @.@  @@.  .@.  .@.  @.@  @.@ @.@.@ .@.  .@.  .@.  @..  .@.  ..@  ...  ... "  # 5x
        " @..  @@.  @.@  ..@  .@.  @.@  @.@ @.@.@ @.@  .@.  @..  @..  ..@  ..@  ...  ... "  # 
        " @..  .@@  @.@  @@.  .@.  .@@  .@. .@.@. @.@  .@.  @@@  @@@  ..@  @@@  ...  @@@ "  #

        #  0    1    2    3    4    5     6   7    8    9    A    B    C    D    E    F     #
    )
    # fmt: on

    @classmethod
    def extract_char(cls, i: int) -> Iterable[str]:
        base_x = i % 0x10
        base_y = (i // 0x10) - 2
        for ln in range(cls.NOMINAL_HEIGHT):
            start = (
                (cls.MAX_WIDTH * base_x)
                + (ln * cls.MAX_WIDTH * 0x10)
                + (base_y * cls.MAX_WIDTH * cls.NOMINAL_HEIGHT * 0x10)
            )
            end = start + cls.MAX_WIDTH
            segment = cls._DATA[start:end]
            yield segment


class Char:
    def __init__(self, s: Iterable[str], crop=True, code: int = None):
        if crop:
            self._map = [c.strip() for c in s]
        else:
            self._map = [*s]
        self._origin = None

        if code is not None:
            self._origin = chr(code)

        if len({*map(len, self._map)}) > 1:
            char = f" for 0x{code:02X} ({chr(code)}):" if code is not None else ":"
            get_logger().warning(f"Inconsistent char map{char} {self._map}")

    def __len__(self) -> int:
        return max(len(line) for line in self._map)

    @property
    def height(self) -> int:
        return len(self._map)

    def generator(self) -> typing.Generator:
        yield from self._map

    @classmethod
    def make_debug(cls, c: "Char") -> "Char":
        if not c._origin:
            raise pt.LogicError("Abstract chars should not have debug versions")
        line_tpl = "[{:s}{:s}]"
        lines = []
        for ln_idx in range(CharMap.NOMINAL_HEIGHT):
            lines.append(line_tpl.format(c._origin, to_superscript(str(ln_idx))))
        return Char(lines)


CHARS = {chr(k): Char(CharMap.extract_char(k), code=k) for k in range(0x20, 0x60)}
CHARS_DEBUG = {k: Char.make_debug(v) for (k, v) in CHARS.items()}

C_EMPTY = Char([""] * CharMap.NOMINAL_HEIGHT)
C_UNDEF = lambda c: Char([":"] * (CharMap.NOMINAL_HEIGHT - 1) + [c], crop=False, code=ord(c))
C_SEP = Char(["."] * CharMap.NOMINAL_HEIGHT)
