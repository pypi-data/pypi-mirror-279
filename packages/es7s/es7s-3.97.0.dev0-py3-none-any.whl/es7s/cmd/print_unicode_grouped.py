# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re
import unicodedata
from collections import deque
from dataclasses import dataclass

import pytermor as pt
from es7s_commons.column import _dcu
from holms.core import CategoryStyles, Attribute, Options, Char
from holms.core.writer import Row, Column, get_view, CHAR_PLACEHOLDER
from holms.db import resolve_category, find_block, UnicodeBlock

from ._base import _BaseAction
from ..shared import get_stdout, get_logger


@dataclass
class CharGroup:
    categ: str
    blk: UnicodeBlock
    values: list[str]

    def append(self, val):
        self.values.append(val)


class action(_BaseAction):
    def __init__(self, *args, **kwargs):
        self._catstyles = CategoryStyles()
        self._render_name = lambda c: get_view(Attribute.NAME).render(
            Options(),
            Row(c, 0, 0),
            Column(Attribute.NAME, 0, 0),
        )
        self._run(*args, **kwargs)

    def _run(self, start: int, end: int):
        if end < start:
            end = start + 0xFF
        prev_categ = None
        prev_blk = None
        chars = [*map(chr, range(start, end + 1))]
        queue = deque()

        while chars:
            categ = None
            blk = None
            if c := chars.pop(0):
                categ = unicodedata.category(c)
                blk = find_block(ord(c))
            if (
                prev_categ
                and prev_blk
                and categ
                and blk
                and (prev_categ[0] != categ[0] or prev_blk != blk)
            ):
                queue.append(CharGroup(prev_categ, prev_blk, []))
            prev_categ = categ
            prev_blk = blk
            if c:
                if not queue:
                    queue.append(CharGroup(categ, blk, []))
                queue[-1].append(c)

        prev_blk = None
        for grp in queue:
            if not prev_blk or grp.blk != prev_blk:
                if prev_blk:
                    get_stdout().echo()
                get_stdout().echo(
                    f"{pt.LINE_DOUBLE.b}[{grp.blk.abbr}]"
                    + pt.fit(
                        f" {grp.blk.name} ",
                        88,
                        "^",
                        fill=pt.LINE_DOUBLE.b,
                    )[len(grp.blk.abbr) + 3 :]
                    + "\n"
                )

                prev_blk = grp.blk
            self._print_categ(grp.values, grp.categ, grp.blk)

    def _ucs(self, c) -> str:
        return f"U+{ord(c):X}"

    def _print_categ(self, g, categ, blk: UnicodeBlock):
        if not g or not categ or not blk:
            return

        def _p(c):
            return get_stdout().render(
                f"[{self._ucs(c)} {self._render_name(Char(c)).strip()}]", pt.cv.GRAY_30
            )

        def _c(c):
            try:
                cat_abbr = unicodedata.category(c)
                cat = resolve_category(cat_abbr[0])
            except ValueError as e:
                get_logger().warning(f"Failed to determine category of {c!r}: {e}")
                return "?"
            st = self._catstyles.get(cat_abbr)
            return get_stdout().render(cat.name, st)

        start = _p(g[0])
        end = None if len(g) < 2 else _p(g[-1])
        bounds = [*map(str.expandtabs, pt.filtern((start, end)))]
        max_len = max(len(_dcu(b)) for b in bounds)
        chars = [Char(c) for c in g]
        assigned = [c for c in chars if not c.is_invalid and not c.is_unassigned]
        counts = (len(chars),)
        cat = _c(g[0])
        cc = pt.pad(4) + "{}× {} ".format(*counts, _dcu(cat))
        title = cc + bounds[0]

        label = pt.LINE_SINGLE.make(
            min(80, len(g) + 4),
            ["".join(line) for line in pt.chunk([self._print_char(G) for G in g], 76)],
        )
        label = [*label]
        stdout = get_stdout()
        stdout.echo(title.replace(_dcu(cat), cat))
        [stdout.echo(pt.pad(4) + line) for line in label]
        stdout.echo("")

    def _print_char(self, c: Char | str) -> str:
        if not isinstance(c, Char):
            c = Char(c)
        if c.should_print_placeholder:
            return CHAR_PLACEHOLDER
        return c.value
