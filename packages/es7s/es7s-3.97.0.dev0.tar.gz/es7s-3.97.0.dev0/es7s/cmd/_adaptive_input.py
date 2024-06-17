# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from __future__ import annotations

import re
import sys
from io import TextIOBase, UnsupportedOperation
from pathlib import Path
from pty import STDIN_FILENO
from typing import TextIO, Iterable

import pytermor as pt

from es7s.shared import get_logger, get_stderr


class _AdaptiveInputAction:
    def __init__(
        self,
        *,
        file: tuple[TextIOBase],
        stdin: bool,
        input: tuple[str] = (),
        demo: bool = None,
        null: bool = None,
        add_eof: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._init_inputs(
            arg_inputs=[*input],
            opt_files=[*file],
            opt_stdin=stdin,
            opt_demo=demo,
            opt_null=null,
            add_eof=add_eof,
            **kwargs,
        )

    def _get_demo_input(self) -> Path | None:
        """@overrideable"""
        raise NotImplementedError(f"No demo is defined for {self}")

    def _get_default_file(self) -> TextIOBase | None:
        """@overrideable"""
        return None

    def _init_inputs(
        self,
        arg_inputs: list[str],
        opt_files: list[TextIO],
        opt_stdin: bool,
        opt_demo: bool,
        opt_null: bool,
        add_eof: bool,
        **_,
    ):
        stdin = self._get_stdin()
        stdin_specified = stdin in opt_files
        if opt_stdin and not stdin_specified:
            opt_files += [self._get_stdin()]

        if not opt_files and (default_file := self._get_default_file()):
            opt_files += [default_file]

        inputs_raw = []
        if opt_demo:
            if demo_input := self._get_demo_input():
                with open(demo_input) as f:
                    inputs_raw.append([*self._read_input(f, opt_null)])

        elif arg_inputs:  # no -F/-S  --> read args
            if len(arg_inputs) > 1 and not re.search(r"[ \n]", "".join(arg_inputs)):
                # meld args into one single arg when provided in a cmdline
                # without spaces or newlines *inside* of each, e.g.:
                #
                #         'app 1 2 3' -> ['1 2 3']          joined ['1', '2', '3']
                #       'app "1 2" 3' -> ['1 2', '3']       no action performed
                #    'app 1 2$'\n' 3' -> ['1', '2', '3']    no action performed
                #
                inputs_raw = [[" ".join(arg_inputs)]]
            else:
                inputs_raw = [arg_inputs]

        elif opt_files:  # -F or -S  --> ignore args
            get_logger().debug(f"File is specified - ignoring args")
            for f in opt_files:
                inputs_raw.append([*self._read_input(f, opt_null)])
                if not f.closed:
                    try:
                        if f.fileno() != STDIN_FILENO:
                            f.close()
                    except UnsupportedOperation:
                        pass

        else:
            get_logger().debug(f"No valid data sources")
            self._exit_with_empty_input_msg()
            return

        if not inputs_raw:
            self._exit_with_empty_input_msg()

        self._input_lines: list[str | None] = []
        for input_raw in inputs_raw:
            for line in pt.filtere(map(str.strip, input_raw)):
                line_pp = self._postprocess_input_line(line)
                self._input_lines.append(line_pp.strip())
            if add_eof:
                self._input_lines.append(None)

    def _get_input_lines(self) -> list[str]:
        return self._input_lines

    def _exit_with_empty_input_msg(self):
        get_stderr().echo("Empty input")
        raise SystemExit(1)

    @classmethod
    def _get_stdin(cls) -> TextIO:
        return sys.stdin

    @property
    def stdin_is_tty(self):
        return self._get_stdin().isatty()

    @classmethod
    def _print_prompt(cls, file: TextIO, text="", nl=None, reset=False):
        if cls.stdin_is_tty and file.isatty():
            pfx = ("", "\r")[reset]
            nl = (not reset) if nl is None else nl
            get_stderr().echo(pfx + text, nl=nl)

    def _read_input(self, file: TextIO, opt_null: bool) -> Iterable[str]:
        """
        Yield lines from `file`, max is determined by `_get_input_limit()`.
        If file is a tty, stop reading after two consecutive empty lines.
        """
        sep = "\0" if opt_null else "\n"
        get_logger().debug(f"Reading from: {file}")
        self._print_prompt(file, "Enter input string(s) manually (empty/EOT=stop):")

        empty_lines_in_a_row = 1
        limit_chr = self._get_input_limit()
        while limit_chr is None or limit_chr > 0:
            self._print_prompt(file, "> ", reset=True)

            prevpos = None
            if file.seekable():
                prevpos = file.tell()
            if not opt_null:
                line = file.readline()
            else:
                line = file.read()

            if len(line) == 0 or (file.isatty() and line == sep):
                empty_lines_in_a_row += 1
                if empty_lines_in_a_row > 1:
                    break
                continue
            empty_lines_in_a_row = 1

            line = line.rstrip(sep)
            if prevpos and file.tell() == prevpos:  # EOF reached
                break

            if limit_chr is not None:
                limit_chr -= len(line)
                if limit_chr < 0:
                    get_logger().warning("Max size exceeded, truncating input")
                    yield line[:-limit_chr]
                    break

            if opt_null:
                yield from line.split(sep)
            else:
                yield line

        self._print_prompt(file)

    def _get_input_limit(self) -> int | None:
        """
        :return:  max input length (in chars) (None=no limit).
        """
        return None

    def _postprocess_input_line(self, s: str) -> str:
        """@overrideable"""
        return s
