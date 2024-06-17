# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from __future__ import annotations

import os.path
import re
import tempfile
import typing
from typing import Sized

import pytermor as pt
from es7s_commons import Regex, columns, TextStat

from es7s.shared import get_logger, get_stdout
from ._foreign import Pager


class TemplateCommand:
    REGEX_SECTION_START = "\x1b\x1e"
    REGEX_SECTION_END = "\x1b\x7f"
    REGEX_SUBSTITUTE_SEP = Regex(R"[\t ]*\x1f[\t ]*")

    @typing.overload
    def __init__(self, content: str | bytes):
        ...

    @typing.overload
    def __init__(self, filepath: str):
        ...

    def __init__(self, *args):
        if not args:
            raise ValueError(
                f"Expected 1 argument, got {len(args) if isinstance(args, Sized) else 'None'}"
            )
        if os.path.exists(args[0]):
            filepath = args[0]
            get_logger().debug(f"Input filepath: '{filepath}'")
            with open(filepath, "rt") as f:
                self._tpl = f.read()
        else:
            self._tpl = args[0]

        self._expr_count = 0
        get_logger().debug(f"Input size: " + pt.format_si_binary(len(self._tpl)))

    def run(self, **kwargs):
        engine = pt.TemplateEngine()
        data, postprocessors = self._split(self._tpl)
        substituted = engine.substitute(data)
        columned, ts = columns(substituted.splitlines(), **kwargs)
        rendered = columned.render(get_stdout().renderer)
        postprocessed = self._postprocess(rendered, postprocessors)
        self._print(postprocessed, ts)

    def _split(self, data: str) -> tuple[str, list[str]]:
        if self.REGEX_SECTION_START not in data:
            return data, []

        data, _, postprocessors = data.partition(self.REGEX_SECTION_START)
        postprocessors, _, _ = postprocessors.partition(self.REGEX_SECTION_END)
        return data.rstrip("\n"), postprocessors.splitlines()

    def _postprocess(self, columned: str, postprocessors: list[str]) -> str:
        for pp in postprocessors:
            if not pp:
                continue
            sub_args = [*self.REGEX_SUBSTITUTE_SEP.split(pp, 1)]
            if len(sub_args) != 2:
                get_logger().warning(f"Invalid substitute directive: {pp!r}")
                continue
            try:
                columned = self._postprocess_apply_subexp(columned, sub_args)
            except RuntimeError as e:
                get_logger().exception(e)
                continue

        return columned

    def _postprocess_apply_subexp(self, rendered: str, sub_args: list):
        self._expr_count += 1
        pattern, repl = sub_args
        replacer = self._replacer(repl)

        get_logger().debug(f"Processing expr #{self._expr_count}: '{pattern}' -> '{repl}'")
        get_logger().trace(repr(pattern), label=f"expr {self._expr_count}  search")
        get_logger().trace(repr(repl), label=f"expr {self._expr_count} replace")
        try:
            return re.sub(pattern, replacer, rendered)
        except re.error as e:
            raise RuntimeError(f"Failed to apply substitute expression #{self._expr_count}") from e

    def _replacer(self, repl: str) -> typing.Callable[[re.Match], str]:
        match_count = 0

        def _internal(m: re.Match) -> str:
            nonlocal match_count
            match_count += 1
            inp = m.group()

            debug_label = "New match for expr #{}".format(self._expr_count, match_count)
            trace_label = "expr {} match {}".format(self._expr_count, match_count)
            grps_str = ""
            if m.groups():
                grps_str = f" in {len(m.groups())} group" + (("", "s")[len(m.groups()) > 1])
            if inp:
                debug_label += f", length {len(inp)}{grps_str}: " + pt.cut(
                    repr(inp), 64, overflow="… (truncated)"
                )
            get_logger().debug(debug_label)

            _trace(inp, m.span(), trace_label, "input")
            for idx, grp in enumerate(m.groups()):
                _trace(grp, m.span(idx + 1), trace_label, idx + 1)

            result = m.expand(repl)
            _trace(result, None, trace_label, "output")
            return result

        def _trace(
            data: str, span: tuple[int, int] | None, base_label: str, idx: str | int = None
        ) -> None:
            trace_label = base_label
            if isinstance(idx, int):
                idx = "group {}".format(idx)
            span_str = ""
            if span:
                if span == (-1, -1):
                    span = ()
                span_str += f", span=({(','.join(map(str, span)))})"
            trace_label += " {} (len={}{})".format(idx, len(data) if data else 0, span_str)
            get_logger().trace(repr(data or ""), label=trace_label, skip_empty=False)

        return _internal

    def _print(self, columned: str, ts: TextStat):
        get_logger().debug(ts)

        if not get_stdout().io.isatty():
            get_stdout().echo(columned, nl=False)
            return

        tmp_file = open(tempfile.mkstemp()[1], "w")
        tmp_file.write(columned)
        tmp_file.flush()
        Pager(ts.max_row_len).open(tmp_file)
