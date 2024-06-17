#!/bin/env python3
# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import enum
import os
import re
import shutil
import sys
import typing as t
from collections import namedtuple
from dataclasses import dataclass
from textwrap import TextWrapper

# NO EXTERNAL DEPENDENCIES!


try:
    from ._base import _BaseAction
    from es7s.shared import get_stdout
except ImportError:

    class _Stdout:
        @staticmethod
        def echo(s, nl):
            return print(s, end=["", "\n"][nl])

    get_stdout = lambda: _Stdout

    class _BaseAction:
        ...


COLUMNS = [
    "name",
    "ver",
    "dt",
    "desc",
]


@dataclass
class Package:
    name: str = ""
    dt: str = None
    ver: str = None
    desc: str = None
    match: str = None
    nonmatch: str = None


style = namedtuple("style", ["align", "start", "end", "regex"], defaults=["", "", None])


class ColStyle(style, enum.Enum):
    name = style(">", "\x1b[97m", "\x1b[39m", None)
    dt = style("<", "\x1b[32m", "\x1b[39m", None)
    ver = style("<", "\x1b[1;34m", "\x1b[22;39m", re.compile(R"\d+"))
    desc = style("<", "\x1b[37m", "\x1b[39m", None)
    match = style("<", "", "", None)
    nonmatch = style("<", "\x1b[33m", "\x1b[39m", None)


REGEX = re.compile(
    r"""
    ^ 
    \s* [{ ]+
    (?P<name> [\w_-]+) 
    [ }]+ \s* 
    \[
        (?:[\s.-]*)? (?P<dt> \d{2,4}.\d{1,2}.\d{1,2} )?
        (?:[\s.-]*)? (?i: v?\.?(?:er)?\.?(?:sion)? ) 
        (?:[\s.-]*)? (?P<ver> [\d\s.-]* \d )? 
        (?:[\s.-]*)? (?P<desc> .+? )?
    ]
     .*
    """,
    flags=re.VERBOSE,
)


class action(_BaseAction):
    PFX = "/usr/share/texlive/texmf-dist/tex/"
    DIRS = [
        PFX + "generic",
        PFX + "latex",
        PFX + "plain",
    ]

    def __init__(self, full: bool, **kwargs):
        self._full = full
        self._run()

    def _run(self):
        self._files = [f for d in self.DIRS for f in self._iterdir(d)]
        self._pkgs = []
        self._wrapper = TextWrapper()

        for file in self._files:
            self._determine_version(file)
        self._print()
        self._print_summary()

    def _iterdir(self, path: str) -> t.Iterable[str]:
        for f in os.listdir(path):
            p = os.path.join(path, f)
            if os.path.isfile(p) and p.endswith("sty"):
                yield p
            elif os.path.isdir(p):
                yield from self._iterdir(p)

    def _determine_version(self, path: str):
        with open(path, "rt", errors="replace") as f:
            content = f.read()
        if "\\ProvidesPackage" not in content:
            return
        _, _, content = content.partition("\\ProvidesPackage")
        content, br, _ = content.partition("]")
        content = re.sub(r"[%\s]+|\\\w+", " ", content + br)
        pp = REGEX.sub(self._register_package, content)
        if pp.strip():
            self._pkgs.append(Package(os.path.basename(path), nonmatch=pp))

    def _register_package(self, m: re.Match) -> str:
        self._pkgs.append(Package(**m.groupdict(), match=m.group(0)))
        return ""

    def _print(self):
        def align(s, n, a):
            if a == "^":
                return s.center(n)
            if a == ">":
                return s.rjust(n)
            return s.ljust(n)

        SEP = "  "

        attrs = [s for s in Package.__dict__ if not s.startswith("_")]
        del attrs[attrs.index("match")]
        del attrs[attrs.index("nonmatch")]

        columns = {attr: max(len(getattr(p, attr) or "") for p in self._pkgs) for attr in attrs}
        if not self._full:
            columns["name"] = 16
            columns["ver"] = 6
        termw = shutil.get_terminal_size((120, 25)).columns - 2
        freew = termw - len(SEP) * (len(columns) - 1)
        first_col = next(iter(columns.keys()))

        cursor = 0
        for key, maxw in columns.items():
            if cursor >= freew:
                columns[key] = 0
            cursor += maxw
            if cursor > freew:
                columns[key] -= max(0, cursor - freew)

        for pkg in sorted(self._pkgs, key=lambda p: p.name):
            if pkg.nonmatch:
                name: str = pkg.name.rjust(columns[first_col])
                self._echo(name + SEP)

                self._wrapper.width = termw - len(SEP)
                self._wrapper.initial_indent = " " * (columns[first_col] + len(SEP))
                self._wrapper.subsequent_indent = self._wrapper.initial_indent
                line = (
                    ColStyle.nonmatch.start
                    + self._wrap(pkg.nonmatch.strip()).lstrip()
                    + ColStyle.nonmatch.end
                )
                self._echo(line, nl=True)
                continue

            cursor = 0
            for key in COLUMNS:
                maxw = columns.get(key, None)
                if maxw == 0:
                    continue

                val_orig = getattr(pkg, key)
                val = str(val_orig)
                cval = val
                pad = 0
                if key != "desc":
                    cval = val[:maxw]
                    if len(val) > len(cval):
                        cval = cval[:-1] + "…"
                    pad: int = max(0, maxw - len(cval))

                if key != first_col:
                    self._echo(SEP)
                    cursor += len(SEP)

                if val_orig is None or not val_orig or val_orig.isspace():
                    cval = align("--", maxw, "<")
                    cval = f"\x1b[2m{cval}\x1b[22m"
                    print(cval, end="")
                    cursor += maxw
                    continue

                if key == "desc":
                    self._wrapper.width = termw
                    self._wrapper.initial_indent = " " * cursor
                    self._wrapper.subsequent_indent = " " * cursor
                    cval = self._wrap(cval).lstrip()

                st: style = getattr(ColStyle, key, None)
                cval = align(cval, len(cval) + pad, st.align)
                if st:
                    if st.regex:
                        cval = st.regex.sub(lambda m: st.start + m.group(0) + st.end, cval)
                    else:
                        cval = st.start + cval + st.end
                else:
                    align(cval, len(cval) + pad, "<")
                self._echo(cval)
                cursor += maxw
            self._echo(nl=True)

    def _print_summary(self):
        self._echo("-" * 80, nl=True)
        # fmt: off
        lines = (
            ("\x1b[1m",     "Files with .sty extension:", self._files),
            ("\x1b[1;90m",  "  ├─>" + " Classified as non-package:", len(self._files) - len(self._pkgs)),
            ("\x1b[1m",     "  └─>" + " Packages detected:", self._pkgs),
            ("\x1b[1;34m",  "      ├─>" + " Versions recognised:", [*filter(lambda p: p.ver, self._pkgs)]),
            ("\x1b[1;90m",  "      ├─>" + " Marked as unversioned:", [*filter(lambda p: not p.ver and p.match, self._pkgs)]),
            ("\x1b[1;33m",  "      └─>" + " Chocked on:", [*filter(lambda p: p.nonmatch, self._pkgs)]),
        )
        # fmt: on
        for line in lines:
            fmt, desc, val = line
            self._echo(desc.ljust(32) + fmt)
            self._echo("{:>6d}".format(len(val) if not isinstance(val, int) else int(val)))
            self._echo("\x1b[m", nl=True)

        self._echo(nl=True)
        if not self._full:
            self._echo("Note: -f|--full can be used to disable all collapsing.")

    @staticmethod
    def _echo(s: str = "", nl=False):
        if not sys.stdout.isatty():
            s = re.sub(R"\x1b\[[\d:;]+[a-zA-Z]", "", s)
        if not s and not nl:
            return
        get_stdout().echo(s, nl=nl)

    def _wrap(self, s: str) -> str:
        lines = self._wrapper.wrap(s)
        if not self._full:
            return lines[0].strip() if lines else ""
        return "\n".join(lines)


if __name__ == "__main__":
    kwargs = {
        "full": ("-f" in sys.argv or "--full" in sys.argv),
    }
    action(**kwargs)
