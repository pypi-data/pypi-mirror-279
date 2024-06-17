# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import random
from copy import copy
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

import pytermor as pt

from es7s.shared import get_logger, Styles, get_stdout, pt_, get_demo_res
from ._adaptive_input import _AdaptiveInputAction
from ._base import _BaseAction


@dataclass
class _ColorDef:
    raw_val: str | None
    chain: list[str]
    comment: str | None


class action(_AdaptiveInputAction, _BaseAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._run()

    def _get_demo_input(self) -> Path:
        idx = random.randint(1, 2)
        return get_demo_res(f"demo-tg-{idx}.tdesktop-palette")

    def _run(self):
        self._defs: dict[str, tuple[str, str | None]] = dict()
        self._links = dict()

        for line in self._input_lines:
            if ":" not in line or line.startswith("//"):
                continue
            comment = None
            if "//" in line:
                line, _, comment = line.partition("//")
                comment = comment.strip()

            try:
                name, val = line.split(":")
                self._defs.update({name.strip(): (val.strip().removesuffix(";"), comment)})
            except ValueError:
                get_logger().warning(f"Malformed color definition: {line!r}")

        if not self._defs:
            self._exit_with_empty_input_msg()
        M = max(map(len, self._defs.keys()))

        results: dict[str, _ColorDef] = dict()
        for k in self._defs:
            cdef = self._resolve(k)
            results.update({k: cdef})

        for k, cdef in results.items():
            cc = int(cdef.raw_val, 16)
            a = 255
            if len(cdef.raw_val) > 6:
                a = cc & 0xFF
                cc >>= 8

            links_num = self._links.get(cdef.chain[0], 0)

            prim_col = pt.NOOP_COLOR
            links_col = pt.NOOP_COLOR
            if links_num > 0:
                if len(cdef.chain) > 1:
                    prim_col = pt.cvr.METALLIC_BLUE
                    links_col = pt.cv.YELLOW
                else:
                    prim_col = pt.cvr.AIR_SUPERIORITY_BLUE
            elif len(cdef.chain) > 1:
                prim_col = Styles.TEXT_DEFAULT.fg

            chain: list[str] = copy(cdef.chain)
            for (idx, key) in enumerate(chain):
                if idx == 0:
                    chain[idx] = pt.Fragment(key.rjust(M), pt.Style(fg=prim_col, bold=True))
                else:
                    chain[idx] = " ← " + key

            links_w = 4
            if links_num > 0:
                links_fg = pt.Composite(
                    pt.Fragment(f" +{links_num}".ljust(links_w), pt.Style(fg=links_col))
                )
            else:
                links_fg = pt.pad(links_w)
            chain.insert(1, links_fg)

            cbox = pt_.format_colorbox(cc, a)
            cbox += *chain,
            if cdef.comment:
                cbox += (pt.pad(2) + "// " + cdef.comment or "", Styles.TEXT_LABEL)
            get_stdout().echo_rendered(cbox)

    def _resolve(self, k, stack=None) -> _ColorDef:
        if not stack:
            stack: list[str] = []
        stack.append(k)

        if k not in self._defs.keys():
            return _ColorDef(None, stack, None)

        v, com = self._defs.get(k)
        if v.startswith("#"):
            return _ColorDef(v[1:], stack, com)

        if v not in self._links.keys():
            self._links[v] = 0
        self._links[v] += 1

        return self._resolve(v, stack)
