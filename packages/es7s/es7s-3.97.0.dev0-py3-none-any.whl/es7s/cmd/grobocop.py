# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import unicodedata
from collections.abc import Iterable

import pytermor as pt
from es7s_commons import columns
from holms.db import resolve_ascii_cc

from es7s.shared import (
    get_app_config_yaml,
    get_stdout,
    with_terminal_state,
    ProxiedTerminalState,
    get_logger,
    GrobocopStyles,
)
from ._base import _BaseAction

LTR_CHAR = "\u200e"
CHRCOL_NUM = 16


class action(_BaseAction):
    def __init__(
        self, codepage: tuple[str] | list[str], all: bool, list: bool, wide: bool, codes: bool
    ):
        self.COL_WIDTH = (3, 4)[wide]
        if codes:
            self.COL_WIDTH = 6
        self.MARGIN_LEFT = self.COL_WIDTH
        self.MARGIN_RIGHT = self.COL_WIDTH

        _, self._cp_config = get_app_config_yaml("codepages")
        self._cp_names, self._cp_defs = self._make_map(self._cp_config)
        self._styles = GrobocopStyles()
        self._wide = wide
        self._codes = codes

        input_cps = codepage
        if all:
            input_cps = [*self._cp_names]
        elif not codepage:
            input_cps = ["ascii"]

        if list:
            self._print_list(list, all)
            return

        input_cps = [*map(str.lower, input_cps)]
        for input_cp in input_cps:
            if input_cp not in self._cp_defs.keys():
                raise RuntimeError(
                    f"Unknown codepage: {input_cp!r}. See supported codepages with '--list'"
                )

        run_fn = with_terminal_state(tabs_interval=self.COL_WIDTH)(self._run)
        run_fn(input_cps=input_cps)

    def _make_map(self, cp_cofnig: dict) -> tuple[list[str], dict[str, dict[str]]]:
        cp_config_codepages: list[dict] = cp_cofnig.get("codepages")
        cp_config_overrides: dict[str, dict[int, str]] = cp_cofnig.get("overrides")

        cp_names = list()
        cp_defs = dict()
        for cp in cp_config_codepages:
            code = cp.get("code").lower()
            if override_key := cp.get("overrides"):
                cp.update({"overrides": cp_config_overrides.get(override_key)})
            cp_names.append(code)
            for tfn in [
                lambda s: s,
                lambda s: s.replace("_", "-"),
                lambda s: s.replace("_", ""),
            ]:
                tcode = tfn(code)
                cp_defs[tcode] = cp
                for a in cp.get("aliases", []):
                    ta = tfn(a).lower()
                    cp_defs[ta] = cp_defs[tcode]
        return cp_names, cp_defs

    def _print_list(self, list: bool, all: bool):
        alias_prefix = ""
        if get_stdout().isatty():
            alias_prefix = "  => "
        if list:
            if all:
                supported = []
                for name in self._cp_names:
                    supported.append(name)
                    for alias in self._cp_defs[name].get("aliases", []):
                        supported.append(alias_prefix + alias.lower())
            else:
                supported = self._cp_names

            get_stdout().echo("\n".join(supported))

    def _run(self, termstate: ProxiedTerminalState, input_cps: list[str]):
        lines = []
        sectsize = None
        for cp in input_cps:
            sect = self._print_cp(cp)
            if not sectsize:
                sectsize = len(sect)
            elif sectsize != len(sect):
                raise RuntimeError(f"Inconsistent sections sizes: {sectsize}, {len(sect)}")
            lines.extend(sect)

        c, ts = columns(
            lines,
            sectsize=sectsize,
            gap=["", "\t"][self._wide],
            sectgap=[0, 1][self._wide],
            tabsize=self.COL_WIDTH,
        )
        get_stdout().echoi_rendered(c)
        get_logger().debug(ts)

    def _print_cp(self, cp: str) -> list[str]:
        result = [
            self._format_top(cp),
            *self._format_main(cp, self._cp_defs.get(cp).get("overrides")),
            *self._format_bottom(),
        ]
        return result

    def _format_top(self, codepage: str) -> pt.Text:
        cpdef = self._cp_defs[codepage]

        max_len = self.COL_WIDTH * CHRCOL_NUM
        # if self._wide:
        max_len += self.MARGIN_LEFT + self.MARGIN_RIGHT
        space_left = max_len
        result = pt.Text()

        cp_el = (
            codepage,
            len(codepage) + self.MARGIN_LEFT + self.MARGIN_RIGHT,
            "^",
            self._styles.SUB_BG,
        )

        alias_el = None
        if self._wide:
            alias_vis = cpdef.get("alias_vis", pt.pad(self.MARGIN_LEFT))
            if not alias_vis.isspace():
                alias_vis = f"({alias_vis})"
            alias_w = len(alias_vis)
            alias_el = (alias_vis, alias_w + 2, "^", self._styles.BG)

        if self._wide:
            lang_el = (
                ", ".join(cpdef.get("languages", ["*"])) + pt.pad(self.MARGIN_RIGHT),
                None,
                ">",
                self._styles.AXIS,
            )
        else:
            lang_el = ("", None, None, self._styles.BG)

        for el in [cp_el, alias_el, lang_el]:
            if not el:
                continue
            string, w, align, st = el
            if w is None:
                w = space_left
                space_left = 0
            result += pt.Fragment(pt.fit(string, w, align=align), st)
            space_left = max(0, space_left - w)
            if space_left == 0:
                break

        return result

    def _format_bottom(self) -> Iterable[pt.Text]:
        # if not self._wide:
        #     return
        pref = "x" if self._wide else ""
        result = pt.Fragment(pt.fit("", self.MARGIN_LEFT), self._styles.BG)
        for lo in range(0, CHRCOL_NUM):
            result += pt.Fragment(f"{pref}{lo:^X}".center(self.COL_WIDTH), self._styles.AXIS)
        result += pt.Fragment(pt.fit("", self.MARGIN_RIGHT), self._styles.BG)
        yield result
        return

    def _format_main(self, codepage: str, overrides: dict[int, str] = None) -> Iterable[pt.RT]:
        for hi in range(0, CHRCOL_NUM):
            line = ""
            # if  self._wide:
            line += pt.Fragment(f"{hi:X}x".ljust(self.MARGIN_LEFT), self._styles.AXIS)
            for lo in range(0, CHRCOL_NUM):
                st = self._styles.DEFAULT
                i = lo + (hi << 4)
                if overrides and i in overrides.keys():
                    c = overrides.get(i)
                    st = self._styles.OVERRIDE
                else:
                    c = bytes([i]).decode(codepage, errors="replace")
                if c == "�" and (smb := self._sample_multibyte(codepage, i)):
                    c = smb
                    st = self._styles.MULTIBYTE
                c, st = self._format_char(c, st, hi, lo, i)
                if not c.endswith(LTR_CHAR):
                    c = f"{c:^{self.COL_WIDTH}.{self.COL_WIDTH}s}"
                cellw = len(c) if not c.endswith(LTR_CHAR) else len(c[:-1])
                if cellw < self.COL_WIDTH:  # and lo < CHRCOL_NUM-1:
                    c += "\t"
                if st.bg:
                    line += pt.Fragment(c, st)
                else:
                    for frag in pt.apply_style_words_selective(c, st):
                        line += frag
            # if  self._wide:
            line += pt.Fragment(pt.fit("▏", self.MARGIN_RIGHT), self._styles.UNDEFINED)
            yield line

    def _format_char(self, char: str, st: pt.FT, hi: int, lo: int, i: int) -> tuple[str, pt.FT]:
        s, cw = char, 1
        try:
            ucc = unicodedata.category(char)
            cw = pt.guess_char_width(char)
            code = ord(char)
        except TypeError:
            ucc = ""
            s, st = "?", self._styles.ERROR
            code = None

        if ucc.startswith("C"):
            if ucc.startswith("Co"):
                if self._wide:
                    s = pt.cut(f"{ord(s):X}", self.COL_WIDTH)
                else:
                    s = "?"
                st = self._styles.UNASSIGNED
            else:
                st = self._styles.CC

                if char == "\u00AD":
                    s = "SHY"
                elif char == "\u200C":
                    s = "ZWNJ"
                elif char == "\u200D":
                    s = "ZWJ"
                elif char == "\u200E":
                    s = "LRM"
                elif char == "\u200F":
                    s = "RLM"
                else:
                    try:
                        s = resolve_ascii_cc(ord(char)).abbr
                    except LookupError:
                        s, st = "?", self._styles.ERROR

        elif ucc.startswith("Z"):
            st = self._styles.WS
            if char == "\x20":
                s = "SP"
            elif char == "\xa0":
                s = "NBSP"

        elif char == "�":
            s = f"▏{i:02X}".center(self.COL_WIDTH)
            st = pt.Style(self._styles.UNDEFINED, overlined=True, underlined=(hi == CHRCOL_NUM - 1))
            code = None

        elif len(ucc) > 0:
            s = " " * (2 - max(cw, len(char))) + char + LTR_CHAR

        else:
            s, st = "?", self._styles.ERROR

        if self._codes and code:
            s = pt.cut(f"{code:{self.COL_WIDTH}X}", self.COL_WIDTH)

        if (
            (ucc.startswith(("C", "Z")) or (self._codes and code))
            and len(s) > 1
            and (not self._wide or len(s) == self.COL_WIDTH)
        ):
            if (hi - lo) % 2 == 1:
                st = pt.Style(st, dim=True, overlined=True, underlined=True)

        return s, st

    def _sample_multibyte(self, cp: str, i: int) -> str | None:
        size = self._cp_defs[cp].get("size")
        start = 0xB0 if size > 16 else 0xB0
        if size >= 16:
            for j in range(start, 0xFF):
                b = bytes([i, j])
                try:
                    c = b.decode(cp)
                except:
                    pass
                else:
                    return c
        return None
