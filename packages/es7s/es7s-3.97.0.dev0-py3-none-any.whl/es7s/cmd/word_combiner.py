# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re
import time
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from random import shuffle
from statistics import mean

import pytermor as pt

from ._adaptive_input import _AdaptiveInputAction
from ._base import _BaseAction
from es7s.shared import get_stdout, get_res_dir, Styles


@dataclass(frozen=True)
class ResultPart:
    ...


@dataclass(frozen=True)
class Result:
    parts: list[str]


class action(_AdaptiveInputAction, _BaseAction):
    def __init__(self, max_size: int, min_overlap: int, nesting: bool, **kwargs):
        super().__init__(**kwargs)
        self._max_size = max_size
        self._min_overlap = min_overlap
        self._nesting = nesting

        self._run(**kwargs)

    def _get_demo_input(self) -> Path | None:
        return get_res_dir(Path("demo", "demo-word-combiner.txt"))

    def _run(self, **kwargs):
        self._input_lines = [re.sub(R"\W+", "", line).lower() for line in self._input_lines]
        shuffle(self._input_lines)

        self._build_prefix_map()
        self._print_header()

        combos = self._find_combinations()
        self._print_minmax_combinations(combos)

    def _build_prefix_map(self):
        self._PREFIX_MAP = dict()
        for word in self._input_lines:
            for end in range(self._min_overlap, len(word)):
                pfx = word[:end]
                if pfx not in self._PREFIX_MAP.keys():
                    self._PREFIX_MAP[pfx] = []
                self._PREFIX_MAP[pfx].append(word)

    def _find_combinations(self) -> list[tuple[int, pt.RT, str]]:
        combos = list[tuple[int, pt.RT, str]]()
        last_cost_ns = deque[int](maxlen=10)
        show_progressbar = False

        for (inp_idx, first) in enumerate(self._input_lines):
            start_ts = time.monotonic_ns()
            for (parts, end_idxs) in self._find_next_words([first]):
                if not parts or len(parts) != self._max_size:
                    continue
                formatted = pt.Text()
                raw_parts = []
                for pidx, (part, end_idx) in enumerate(zip(parts, end_idxs)):
                    formatted += part[:end_idx]
                    raw_parts += [part]
                combos.append((len(formatted), formatted, " + ".join(raw_parts)))
            end_ts = time.monotonic_ns()
            last_cost_ns.append(end_ts - start_ts)
            eta_ns = mean(last_cost_ns) * (1 - (inp_idx + 1) / len(self._input_lines))
            print(pt.format_time_ns(eta_ns))
        combos.sort(key=lambda r: r[0])
        return combos

    def _find_next_words(self, words: list[str], end_idx: list[int] = None) -> Iterable[list[str]]:
        if end_idx is None:
            end_idx = []

        last_word = words[-1]
        last_end_lpos = self._min_overlap - 1
        if not self._nesting:
            last_end_lpos = max(last_end_lpos, (end_idx or [0])[-1])
        last_end_rpos = len(last_word) - self._min_overlap + 1

        for last_end_idx in range(last_end_lpos, last_end_rpos):
            last_end = last_word[last_end_idx:]
            for next_word in self._PREFIX_MAP.get(last_end, []):
                if next_word in words:
                    continue

                if len(words) >= self._max_size:
                    yield words, [*end_idx, len(last_word)]
                    return

                yield from self._find_next_words([*words, next_word], [*end_idx, last_end_idx])
        yield words, [*end_idx, len(last_word)]

    def _print_header(self):
        overlap_str = str(self._min_overlap)
        header_st = pt.FrozenStyle(underlined=True)
        header_str = []
        for hlabel, hvalue, header_fg_st in [
            ("SIZE", str(self._max_size), pt.DEFAULT_COLOR),
            ("OVERLAP", overlap_str, pt.DEFAULT_COLOR),
            (
                "NESTING",
                ("OFF", "ON")[self._nesting],
                (Styles.TEXT_DISABLED.fg, pt.cv.YELLOW)[self._nesting],
            ),
        ]:
            header_str.extend(
                [
                    (f" {hlabel} ", pt.FrozenStyle(header_st, fg=header_fg_st)),
                    (f"◤ {hvalue} ", pt.FrozenStyle(fg=header_fg_st, inversed=True, bold=True)),
                    ("◢", pt.FrozenStyle(header_st, fg=header_fg_st, inversed=True)),
                ]
            )
        header_tx = pt.Text(*header_str)

        stdout = get_stdout()
        stdout.echoi_rendered(header_tx)
        stdout.echo_rendered(pt.Fragment(pt.pad(len(header_tx)), pt.FrozenStyle(overlined=True)))

    def _print_minmax_combinations(self, combos: list):
        stdout = get_stdout()

        stdout.echo_rendered(f" INPUT ({len(self._input_lines)}) ", pt.FrozenStyle(bold=True))
        stdout.echo(pt.wrap_sgr(" ".join(self._input_lines), 80, 2, 2))

        results_header = f" RESULTS ({len(combos)})"
        stdout.echo_rendered(results_header, pt.FrozenStyle(bold=True))

        if len(combos) == 0:
            return

        min_combo_len = combos[0][0]  # @REFACTORME EAAAUURRGGHHH to dataclasses
        max_combo_len = combos[-1][0]  # @REFACTORME EAAAUURRGGHHH to dataclasses
        MAX_COMBOS_TO_PRINT = 10

        combos_filtered = []
        if len(combos) < MAX_COMBOS_TO_PRINT:
            pass

        # combos_filtered = []
        # for idx, combo in enumerate(combos):
        #     if combo not in combos_filtered:
        #         combos_filtered.append(combo)
        self._print_combinations_filtered(combos, "MIN", pt.cv.GREEN, min_combo_len)

        if max_combo_len == min_combo_len:
            return
        self._print_combinations_filtered(combos, "MAX", pt.cv.RED, max_combo_len)

    def _print_combinations_filtered(self, combos: list, label: str, fg: pt.Color, length: int):
        st = pt.FrozenStyle(fg=fg, bold=True)
        printed = 0
        for combo in combos:
            if combo[0] != length:
                continue

            frags = [
                ["", f"   {label}"][len(combos) > 1],
                " (",
                (f"{combo[0]:2d}", st),
                "): ",
                combo[1],
                (f"  {combo[2]}", Styles.TEXT_LABEL),
            ]
            get_stdout().echo_rendered(pt.Text(*frags))
            printed += 1
            if printed >= 5:
                get_stdout().echo_rendered("   ...")
                break
