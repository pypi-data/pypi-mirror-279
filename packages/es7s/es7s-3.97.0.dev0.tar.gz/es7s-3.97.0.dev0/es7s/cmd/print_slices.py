# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import copy
from dataclasses import dataclass
from functools import cached_property, lru_cache
from math import floor, sqrt

import pytermor as pt
from es7s_commons import Gradient, GradientSegment

from es7s.shared import Styles as BaseStyles, get_stdout
from ._base import _BaseAction


@dataclass(frozen=False)
class _Setup:
    max_sample_length = 64
    autogen_sample_start = "A"
    first_column_pad = 2
    result_gap = 1

    reverse_begin_pos: bool = False
    reverse_begin_neg: bool = False
    reverse_begin_full: bool = False
    reverse_end_pos: bool = False
    reverse_end_neg: bool = False
    reverse_end_full: bool = True
    reverse_step: bool = False


class _Styles(BaseStyles):
    def __init__(self):
        self.REGULAR_CELL = pt.FrozenStyle(fg=pt.cv.GRAY_42)

        inpval_default_bg = pt.cv.GRAY_0
        inpval_default_fg = pt.cvr.ICATHIAN_YELLOW
        self.DEFAULT_INPVAL_CELL = pt.FrozenStyle(self.REGULAR_CELL, bg=inpval_default_bg)
        self.DEFAULT_INPVAL_HEADER = pt.FrozenStyle(fg=inpval_default_fg, bold=True)
        self.DEFAULT_INPVAL_HEADER_BG = pt.FrozenStyle(bg=inpval_default_fg)

        inpval_first_bg = pt.cvr.DARK_GREEN
        inpval_first_fg = pt.cvr.APPLE_GREEN
        self.FIRST_INPVAL_CELL = pt.FrozenStyle( bg=inpval_first_bg)
        self.FIRST_INPVAL_HEADER = pt.FrozenStyle(fg=inpval_first_fg, bold=True)

        inpval_last_bg = pt.cvr.BLACK_BEAN
        inpval_last_fg = pt.cvr.ELECTRIC_RED
        self.LAST_INPVAL_CELL = pt.FrozenStyle( bg=inpval_last_bg)
        self.LAST_INPVAL_HEADER = pt.FrozenStyle(fg=inpval_last_fg, bold=True)

        self.SAMPLE_GRADIENT = Gradient([
            GradientSegment([0, .5, 1], inpval_first_fg.rgb, inpval_last_fg.rgb),
        ])

        # Incandescent #0
        # if char_pos < 10:
        #     char_rel_pos = char_pos / min(10, self._sample_length)
        #     h, s, v = ((1 - char_rel_pos) * 60, char_rel_pos * 2, 1)
        # else:
        #     h, s, v = (0, 1, 1 - (char_pos - 10) / (self._sample_length - 5))


InputValue = int | None
InputList = list[InputValue]


class action(_BaseAction):
    def __init__(self, length: int | None, sample: str | None):
        self._setup = _Setup()
        self._styles = _Styles()
        self._stdout = get_stdout()

        if sample:
            self._sample = sample
        else:
            self._sample = self._autogenerate_sample(length)
        self._sample = self._sample[: self._setup.max_sample_length]
        self._sample_unique = len(set(self._sample)) == len(self._sample)

        self._INPVAL_BEGIN: InputList = []
        self._INPVAL_END: InputList = []
        self._INPVAL_END_REV: InputList = []
        self._INPVAL_STEP: InputList = [None, -1]

        self._run()

    def _run(self):
        self._fill_inputs()

        self._print_sample()
        self._print_table()

    def _autogenerate_sample(self, length: int | None) -> str:
        """
        We want to make sample as big as possible, but the table it produces
        must fit into current terminal by width and height at the same time.
        Lets determine biggest sample length analytically.

        Assume N is sample length, W is a terminal width and H is its height.
        W and H can be expressed in terms of N like follows::

            (1)      W = (2n + 1) * (n + 1) + 12
                 =>  W = 2n^2 + 2n + n + 2
                 =>  W = 2n^2 + 3n + 14 .

            (2)      H = 2 + 2 + (2n+1) + 1 + (2n+1) + 1
                 =>  H = 4n + 8
                 =>  Nh = (H - 8)/4 .

        The formulas above takes into account full table width with header
        column and rows (but not the "SAMPLE:" header). Solving (1) gives::

            (3)      Nw = 1/4 * (-3 + sqrt(-103 + 8W)) .

        Now we know how many samples will fit in a terminal with given size (W, H)::

            (4)   N = min(Nh, Nw) = |¯ 1/4 * (-3 + sqrt(-103 + 8W)) ,
                                    |_ (H - 8)/4) .
                                    min

        Substituting them with current terminal size gives as the maxiumum sample
        length fitting into it. For example, assume W=120 and H=25::

            N = min( 1/4 * (-3 + sqrt(-103 + 8W)) , (H - 8)/4) )
              = min( 6.57, 4.25 ) = 4.25 .

        Rounding it down gives the result of the maximum sample length that produces
        a table that still fits into (120,25)-sized terminal: 4 chars, which will
        produce a table sized (58,24). Without a requirement to fit the height, sample
        could be of length 6 and the table wolud occupy a (104,32) rectangle.

        """
        if not length:
            import shutil

            max_len_by_w = max(1, floor((-3 + sqrt(-103 + 8 * pt.get_terminal_width(pad=0))) / 4))
            max_len_by_h = max(1, floor((shutil.get_terminal_size().lines - 8) / 4))
            length = min(max_len_by_w, max_len_by_h)

        start_code = ord(self._setup.autogen_sample_start)
        return "".join(map(chr, range(start_code, start_code + length)))

    def _fill_inputs(self):
        range_neg: InputList = [*range(-self._sample_length, 0)]
        range_pos: InputList = [*range(0, self._sample_length+1)]

        def _extend_lists(val_list, reverse_begin: bool, reverse_end: bool):
            _extend_list(self._INPVAL_BEGIN, val_list, reverse_begin)
            _extend_list(self._INPVAL_END, val_list, reverse_end)

        def _extend_list(val_list: InputList, val_range: InputList, reverse: bool):
            val_list.extend([val_range, reversed(val_range)][reverse])

        _extend_lists(range_neg, self._setup.reverse_begin_neg, self._setup.reverse_end_neg)
        self._INPVAL_BEGIN.append(None)
        self._INPVAL_END.append(None)
        _extend_lists(range_pos, self._setup.reverse_begin_pos, self._setup.reverse_end_pos)

        if self._setup.reverse_begin_full:
            self._INPVAL_BEGIN.reverse()
        if self._setup.reverse_end_full:
            self._INPVAL_END.reverse()
        if self._setup.reverse_step:
            self._INPVAL_STEP.reverse()

        self._INPVAL_END_REV = copy.copy(self._INPVAL_END)
        # self._INPVAL_END_REV.append(None)
        # self._INPVAL_END.insert(0, None)

    def _get_begin_inputs(self, step: InputValue) -> InputList:
        return [self._INPVAL_BEGIN, self._INPVAL_BEGIN][step is None]

    def _get_end_inputs(self, step: InputValue):
        return [self._INPVAL_END_REV, self._INPVAL_END][step is None]

    def _format_inpval(self, val: InputValue, omit_none=True, color_spec=True):
        if val is None and not omit_none:
            w = len(str(None))
        else:
            w = self._max_sample_length_width
        st = pt.NOOP_STYLE

        if val is not None:
            s = f"{val:>{w}}"
            # if color_spec:
            #     if val == 0:
            #         return pt.Fragment(s, self._styles.FIRST_INPVAL_HEADER)
            #     if val == -self._sample_length:
            #         return pt.Fragment(s, self._styles.LAST_INPVAL_HEADER)
            return s

        if color_spec:
            if omit_none:
                st = self._styles.DEFAULT_INPVAL_HEADER_BG
            else:
                st = self._styles.DEFAULT_INPVAL_HEADER
        if omit_none:
            s = pt.pad(w)
        else:
            s = "None"[:w]
        return pt.Fragment(s, st)

    def _print_sample(self):
        label = f"SAMPLE ({self._sample_length}): "
        labeled_sample_length = len(label) + self._sample_length
        padding = (self._table_width - labeled_sample_length) // 2
        self._stdout.echo(pt.pad(padding) + label, nl=False)

        result_rt = self._format_result(self._sample, apply_cell_style=False)
        self._stdout.echo_rendered(result_rt)
        self._stdout.echo()

    def _print_table(self):
        self._print_header_row(self._INPVAL_STEP[0])
        self._print_table_separator()

        for step in self._INPVAL_STEP:
            for end in self._get_end_inputs(step):
                self._print_first_col(end, step)
                for begin in self._get_begin_inputs(step):
                    self._print_result(begin, end, step)
                self._stdout.echo()
            self._print_table_separator()

    def _print_header_row(self, step: int):
        b_eq_each_cell = 2 + self._max_sample_length_width <= self._sample_length
        if b_eq_each_cell:
            first_col_label = pt.pad(self._first_col_width + self._setup.first_column_pad)
        else:
            first_col_label = "B=".center(self._first_col_width)
            first_col_label += pt.pad(self._setup.first_column_pad)
        self._stdout.echo(first_col_label, nl=False)

        for val in self._get_begin_inputs(step):
            tx = pt.Text(
                "B=" if b_eq_each_cell else "",
                self._format_inpval(val, omit_none=False),
                width=self._sample_length + self._setup.result_gap,
                align="^",
            )
            self._stdout.echo_rendered(tx, nl=False)
        self._stdout.echo()

    def _print_first_col(self, end: InputValue, step: InputValue):
        end_frg = self._format_inpval(end)
        step_frg = self._format_inpval(step, color_spec=False)
        col_w = self._first_col_width

        frgs = [
            "B",
            ":",
            end_frg,
            " " if step is None else ":",
            step_frg,
        ]
        tx = pt.Text("[", *frgs, "]", width=col_w, align=">")
        self._stdout.echo_rendered(tx, nl=False)
        self._stdout.echo(pt.pad(self._setup.first_column_pad), nl=False)

    def _print_result(self, begin: InputValue, end: InputValue, step: InputValue):
        result = self._sample[begin:end:step]
        result_rt = self._format_result(result, begin, end, step)
        self._stdout.echo_rendered(result_rt + pt.pad(self._setup.result_gap), nl=False)

    def _format_result(
        self,
        result: str,
        begin: InputValue = None,
        end: InputValue = None,
        step: InputValue = None,
        *,
        apply_cell_style=True,
    ) -> pt.RT:
        cell_st = pt.NOOP_STYLE
        if apply_cell_style:
            cell_st = self._styles.REGULAR_CELL
            is_default = (begin is None or end is None)
            # is_begin = (begin == 0 or end == 0)
            # is_end = (begin in (-1,self._sample_length-1) or end in (-1,))
            if is_default:
                cell_st = self._styles.DEFAULT_INPVAL_CELL
            # if is_begin != is_end:
            #     if is_begin:
            #         cell_st = self._styles.FIRST_INPVAL_CELL
            #     if is_end:
            #         cell_st = self._styles.LAST_INPVAL_CELL

        output: list[pt.RT] = []
        for idx_in_result, char in enumerate(result):
            if not apply_cell_style:  ## SAMPLE
                idx_in_result = 0  # all bright
            idx_in_sample = self._sample.index(char)
            colval = self._get_result_color(idx_in_sample, idx_in_result)
            st = pt.Style(cell_st, fg=pt.Color256.find_closest(colval), bold=True)
            output.append(pt.Fragment(char, st))

        empty_char = pt.Fragment("_", cell_st)
        for _ in range(len(output), self._sample_length):
            output.append(empty_char)

        return pt.Composite(*output)

    @lru_cache
    def _get_result_color(self, idx_in_sample: int, idx_in_result: int) -> pt.FT:
        if self._sample_unique:
            char_pos = idx_in_sample/((self._sample_length-1) or 1)
            hsv = self._styles.SAMPLE_GRADIENT.interpolate(char_pos).hsv
            edges = (0, self._sample_length-1)
            if idx_in_result not in edges or idx_in_sample not in edges:
                return self._styles.TEXT_DEFAULT.fg
            return hsv
        return self._styles.TEXT_DEFAULT.fg

    def _print_table_separator(self):
        self._stdout.echo("─" * self._table_width)

    @cached_property
    def _sample_length(self) -> int:
        return len(self._sample)

    @cached_property
    def _max_sample_length_width(self) -> int:
        return len(str(-self._sample_length))

    @cached_property
    def _first_col_width(self):
        return 5 + self._max_sample_length_width * 2

    @cached_property
    def _table_cells_width(self):
        result_width = self._sample_length + self._setup.result_gap
        return len(self._INPVAL_BEGIN) * result_width

    @cached_property
    def _table_width(self):
        return self._first_col_width + self._setup.first_column_pad + self._table_cells_width
