# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import time
from collections.abc import Iterable
from itertools import product

import pytermor as pt
from pytermor import NonPrintsStringVisualizer

from es7s.shared import (
    get_stdout,
    Styles as BaseStyles,
    get_logger,
    run_subprocess,
)
from es7s.shared.pt_ import guess_width
from ._base import _BaseAction

_Results = dict[str, dict[str, dict[str, str]]]


def _sort_formats(fmts: Iterable[str]) -> list[str]:
    def _sorter(c: str) -> int:
        return ord(c.upper()[-1]) * 10 + int(c.islower()) + c.count(":")

    return [*sorted(fmts, key=_sorter)]


_SPECIAL_FORMATS = {"n", "t"}
_FORMATS = [
    f
    for f in _sort_formats(
        [
            *pt.char_range("A", "Z"),
            *pt.char_range("a", "z"),
            *[(":" * n) + "z" for n in range(1, 4)],
        ]
    )
    if f not in _SPECIAL_FORMATS
]
_MAX_FMT_LEN = max(5, *map(len, _FORMATS))

_COL_W = 12
_LC_DEFAULT = "en_US"
_PFX_DEFAULT = ["%", "%_", "%-", "%5", "%_5", "%-5"]
_PFX_CUSTOM = ["%", "%O", "%E"]

_TABLE_LINE = pt.LINE_DOUBLE
_LOC_SEP_LINE = pt.LINE_SINGLE
_HEADER_LINE = pt.LINE_BOLD

_PFX_SEP = " "
_LOC_SEP = _LOC_SEP_LINE.l + " "
_HEAD_SEP = _HEADER_LINE.l + " "


class _Styles(BaseStyles):
    def __init__(self):
        _FORMAT = pt.FrozenStyle(bold=True)
        _VALUE = pt.NOOP_STYLE
        _LOCALE = pt.FrozenStyle(italic=True)

        # is valid?
        self.FORMAT = {
            True: pt.FrozenStyle(_FORMAT, fg=pt.cv.YELLOW),
            False: pt.FrozenStyle(_FORMAT, fg=pt.cv.GRAY_50, bg=pt.cv.GRAY_19),
        }
        # is valid?
        self.VALUE = {
            True: pt.FrozenStyle(_VALUE),
            False: pt.FrozenStyle(_VALUE, fg=pt.cv.GRAY_19),
        }
        # is default?
        self.LOCALE = {
            True: pt.FrozenStyle(_LOCALE),
            False: pt.FrozenStyle(_LOCALE, fg=pt.cv.BLUE),
        }
        # is odd?
        self.ROW_BG = {
            True: pt.FrozenStyle(bg=pt.cv.GRAY_11),
            False: pt.FrozenStyle(bg=pt.cv.GRAY_15),
        }

        self.PFX_HEADER_BG = pt.FrozenStyle(bg=pt.cv.GRAY_0)


class action(_BaseAction):
    _POSTPROCESSOR = NonPrintsStringVisualizer(keep_newlines=False)

    def __init__(self, locale: tuple[str], whitespace: bool, all: bool, **kwargs):
        self._styles = _Styles()
        self._locales = self._validate_input_locales(*locale)

        self._visualize_whitespace = whitespace
        self._show_all = all

        self._ts: float = time.time_ns() / 1e9
        self._results: _Results = {}
        self._valid_fmts: set[str] = set()

        self._run(**kwargs)

    def _validate_input_locales(self, *locales: str) -> list[str]:
        available = {*self._get_available_locales()}
        normalized_prefixes = {av.partition("_")[0].lower(): av for av in available}
        validated = [_LC_DEFAULT]
        for loc in locales:
            if loc not in available:
                loc_nrm = loc.lower()
                if loc_nrm in normalized_prefixes:
                    loc = normalized_prefixes[loc_nrm]
                else:
                    get_logger().warning(f"Skipping unknown locale: {loc}")
                    continue
            validated.append(loc)
        return validated

    def _get_prefixes(self, loc: str):
        if self._is_default_locale(loc):
            return _PFX_DEFAULT
        return _PFX_CUSTOM

    def _get_prefixed_formats(self, loc: str) -> list[tuple[str, str]]:
        return [*product(self._get_prefixes(loc), _FORMATS)]

    def _get_locales_prefixes(self) -> Iterable[tuple[str, str]]:
        for loc in self._locales:
            for pfx in self._get_prefixes(loc):
                yield loc, pfx

    def _get_table_width(self):
        loc_pfx = [*self._get_locales_prefixes()]
        seps = self._apply_separators(len(loc_pfx) * [""])
        return _MAX_FMT_LEN + len(seps) + len(loc_pfx) * _COL_W

    def _get_invalid_formats(self) -> set[str]:
        return {*_FORMATS, *_SPECIAL_FORMATS} - {*self._valid_fmts}

    # noinspection PyShadowingBuiltins
    def _run(self, list: bool):
        if list:
            for loc in self._get_available_locales():
                get_stdout().echo(loc)
            return
        for loc in self._locales:
            self._results[loc] = self._fetch_results(loc)
        self._print_results()

    def _fetch_results(self, loc: str) -> dict[str, dict[str, str]] | None:
        logger = get_logger()
        loc_results = {}
        pref_formats = self._get_prefixed_formats(loc)

        cpout = [*self._invoke_date(loc)]
        lines = len(cpout)
        exp_lines = len(pref_formats)

        if lines != exp_lines:
            logger.warning(f"Inconsistent 'date' output: {lines} lines, expected {exp_lines}")
            return loc_results

        for (pfx, fmt) in pref_formats:
            if fmt not in loc_results.keys():
                loc_results[fmt] = {}

            datestr = cpout.pop(0)
            datestr_norm = datestr.strip()
            if datestr_norm and datestr_norm != pfx + fmt:
                self._valid_fmts.add(fmt)
            else:
                datestr = None
            loc_results[fmt][pfx] = datestr
        return loc_results

    def _invoke_date(self, locale: str) -> Iterable[str]:
        request = "+"
        for pfx in self._get_prefixes(locale):
            for fmt in _FORMATS:
                request += f"{pfx}{fmt}%n"
        cp = run_subprocess(
            "date",
            request,
            f"-d@{self._ts}",
            env={"LC_TIME": locale + ".UTF-8"},
        )
        yield from cp.stdout.replace("%n", "\n").splitlines()

    @classmethod
    def _postprocess_result(cls, value: str) -> str:
        return pt.apply_filters(value, cls._POSTPROCESSOR)

    def _print_results(self):
        stdout = get_stdout()

        self._print_locales_header()
        self._print_prefixes_header()
        self._print_table_part(_TABLE_LINE.l, _HEADER_LINE.t, _TABLE_LINE.r)
        for (fidx, fmt) in enumerate(_FORMATS):
            if fmt in self._valid_fmts or self._show_all:
                self._print_format(fmt, fidx % 2)
        self._print_table_part(_TABLE_LINE.bl, _TABLE_LINE.b, _TABLE_LINE.br)

        stdout.echo("Sample timestamp:   " + str(self._ts))
        stdout.echo("Empty results for:  " + ", ".join(_sort_formats(self._get_invalid_formats())))

    def _print_table_part(self, left: str, mid: str, right: str):
        part_str = left + self._get_table_width() * mid + right
        get_stdout().echo_rendered(pt.Fragment(part_str))

    def _print_locales_header(self):
        row = pt.Composite()
        for loc in self._locales:
            row += _TABLE_LINE.t * len(_LOC_SEP)
            row += self._render_locale_header_cell(loc)
        self._print_table_row(None, row, False, _TABLE_LINE.t)

    def _render_locale_header_cell(self, loc: str) -> pt.RT:
        loc_st = self._styles.LOCALE.get(self._is_default_locale(loc))
        pfxs = self._get_prefixes(loc)
        return pt.Text(
            pt.Fragment(loc, loc_st),
            pt.Fragment(_TABLE_LINE.t),
            width=len(pfxs) * (_COL_W + len(_PFX_SEP)),
            align=">",
            fill=_TABLE_LINE.t,
            pad_styled=False,
        )

    def _print_prefixes_header(self):
        cells = [
            self._render_prefix_header_cell(pfx, "?")
            for loc in self._locales
            for pfx in self._get_prefixes(loc)
        ]
        row = self._apply_separators(cells)
        self._print_table_row(None, row, True)

    def _render_prefix_header_cell(self, pfx: str, fmt: str) -> pt.RT:
        return pt.Text(
            pt.Fragment(pfx, self._apply_prefix_header_bg(self._styles.VALUE.get(True))),
            pt.Fragment(fmt, self._apply_prefix_header_bg(self._styles.FORMAT.get(True))),
            width=_COL_W,
            align="^",
        )

    def _apply_prefix_header_bg(self, base_st: pt.Style) -> pt.Style:
        return base_st.clone().merge_fallback(fallback=self._styles.PFX_HEADER_BG)

    def _print_format(self, fmt: str, is_odd_row: bool):
        cells = []
        for loc in self._locales:
            loc_fmt_results = self._results[loc].get(fmt, {})
            for pfx in self._get_prefixes(loc):
                value = loc_fmt_results.get(pfx)
                cell = self._render_value_cell(pfx + fmt, value, is_odd_row)
                cells.append(cell)

        row = self._apply_separators(cells)
        self._print_table_row(fmt, row, is_odd_row)

    def _print_table_row(self, fmt: str | None, row: pt.RT, is_odd_row: bool, fill: str = None):
        is_corner = fmt is None and fill is not None
        linel = [_TABLE_LINE.l, _TABLE_LINE.tl][is_corner]
        liner = [_TABLE_LINE.r, _TABLE_LINE.tr][is_corner]
        line = pt.Composite(linel, self._render_format_cell(fmt, fill, is_odd_row), row, liner)
        get_stdout().echo_rendered(line)

    def _render_format_cell(self, fmt: str | None, fill: str | None, is_odd_row: bool) -> pt.RT:
        fmt_lbl = fmt or ""
        is_corner = fmt is None
        is_tz_ext = not fmt_lbl.isalnum()
        is_sep = fill is not None
        fill = fill or " "

        valid = fmt in self._valid_fmts
        fmt_st = self._styles.FORMAT.get(valid)
        align = "^"

        if is_sep or is_corner:
            fmt_st = self._styles.LOCALE.get(True)
        else:
            fmt_st = self._apply_row_bg(fmt_st, is_odd_row)
            if is_tz_ext:
                align = ">"
                fmt_lbl += " "

        aligned_fmt = pt.fit(fmt_lbl, _MAX_FMT_LEN, align, fill=fill)
        return pt.Fragment(aligned_fmt, fmt_st)

    def _render_value_cell(self, pfx_fmt: str, value: str | None, is_odd_row: bool) -> pt.RT:
        max_width = _COL_W
        if value is None:
            st = self._apply_row_bg(self._styles.VALUE.get(False), is_odd_row)
            return pt.Fragment(pt.fit(pfx_fmt, max_width, "^"), st)

        if self._visualize_whitespace:
            value = self._postprocess_result(value)

        while (actual_width := guess_width(value)) > max_width:
            value = value[:-1]
        aligned_value = value + " " * max(0, max_width - actual_width)

        st = self._apply_row_bg(self._styles.VALUE.get(True), is_odd_row)
        return pt.Fragment(aligned_value, st)

    def _apply_row_bg(self, base_st: pt.Style, is_odd_row: bool) -> pt.Style:
        return base_st.clone().merge_fallback(fallback=self._styles.ROW_BG.get(is_odd_row))

    def _apply_separators(self, cells: list[pt.RT]) -> pt.Composite:
        line = pt.Composite()
        for (idx, loc) in enumerate(self._locales):
            line += [_LOC_SEP, _HEAD_SEP][idx == 0]
            for _ in self._get_prefixes(loc):
                line += cells.pop(0)
                line += _PFX_SEP
        return line

    @classmethod
    def _is_default_locale(cls, loc: str) -> bool:
        return loc == _LC_DEFAULT

    @classmethod
    def _get_available_locales(cls) -> list[str]:
        cp = run_subprocess("locale", "-a", check=True)
        utf8_locs = []
        for loc in cp.stdout.splitlines():
            if "utf" not in loc.lower():
                continue
            utf8_locs.append(loc.partition(".")[0])
        return [*sorted(utf8_locs)]
