# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import io
import math
import os.path
import re
import sys
import time
from collections import deque, OrderedDict
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cached_property
from typing import BinaryIO

import pytermor as pt
from es7s_commons import Regex
from pytermor import get_terminal_width

from es7s.shared import ESQDB_DATA_PIPE
from es7s.shared import (
    FrozenStyle,
    Styles as BaseStyles,
    get_logger,
    get_stderr,
    get_stdout,
    with_terminal_state,
)
from es7s.shared import ProxiedTerminalState
from es7s.shared.enum import EsqDbMode
from ._base import _BaseAction


@dataclass(frozen=True)
class SeqStyle:
    _primary: pt.RenderColor
    _secondary: pt.RenderColor
    _auxiliary: pt.RenderColor = pt.NOOP_COLOR
    _bg: pt.RenderColor = pt.NOOP_COLOR

    @cached_property
    def escape_byte(self) -> FrozenStyle:
        return FrozenStyle(fg=pt.cv.HI_WHITE, bg=self.bg, bold=True)

    @cached_property
    def classifier(self) -> FrozenStyle:
        return FrozenStyle(fg=self._secondary, bg=self.bg)

    @cached_property
    def final(self) -> FrozenStyle:
        return FrozenStyle(fg=self._primary, bg=self.bg, bold=True)

    @cached_property
    def interm(self) -> FrozenStyle:
        return FrozenStyle(fg=self._secondary, bg=self.bg, bold=True)

    @cached_property
    def param(self) -> FrozenStyle:
        return FrozenStyle(fg=self._secondary, bg=self.bg)

    @cached_property
    def param_sep(self) -> FrozenStyle:
        return FrozenStyle(fg=self._secondary, bg=self.bg, dim=True)

    @cached_property
    def bg(self) -> pt.RenderColor:
        return self._bg

    @cached_property
    def legend(self) -> FrozenStyle:
        return FrozenStyle(fg=self.bg or self._secondary)


class _Styles(BaseStyles):
    def __init__(self):
        self.QUEUE = FrozenStyle(bg=pt.cvr.MIDNIGHT_BLUE)
        self.SBAR_SEP_BG = pt.cvr.SPACE_CADET
        self.SBAR_BG = pt.cvr.DARK_MIDNIGHT_BLUE

        self.SBAR_SEP_BASE = FrozenStyle(fg=pt.cv.GRAY_0, bg=self.SBAR_SEP_BG)
        self.SBAR_BASE = FrozenStyle(fg=pt.cv.GRAY_0, bg=self.SBAR_BG)

        self.CUR_PART_FMT = FrozenStyle(self.SBAR_BASE, fg=pt.cv.HI_BLUE, bold=True)
        self.TOTAL_PARTS_FMT = FrozenStyle(self.SBAR_BASE, fg=pt.cv.BLUE)
        self.LETTERS_FMT = FrozenStyle(self.SBAR_BASE, fg=pt.cv.BLUE, bold=True)

        self.SEQ_NOOP = SeqStyle(pt.DEFAULT_COLOR, pt.DEFAULT_COLOR)
        self.SEQ_SGR = SeqStyle(pt.cv.YELLOW, pt.DEFAULT_COLOR)
        self.SEQ_SGR_RESET = SeqStyle(pt.cv.GRAY_0, pt.cv.GRAY_0, _bg=pt.cv.YELLOW)
        self.SEQ_UNKNOWN = SeqStyle(pt.cv.MAGENTA, pt.cv.MAGENTA, pt.cv.DEEP_PINK_8)
        self.SEQ_CURSOR = SeqStyle(pt.cv.BLUE, pt.cv.BLUE, pt.cv.NAVY_BLUE)
        self.SEQ_ERASE = SeqStyle(pt.cv.RED, pt.cv.RED, pt.cv.DARK_RED_2)
        self.SEQ_PRIVATE = SeqStyle(pt.cv.GREEN, pt.cv.GREEN, pt.cvr.DARK_GREEN)
        self.SEQ_CURSOR_FP = SeqStyle(pt.cv.CYAN, pt.cv.CYAN, pt.cvr.DARK_CYAN)

        self.PART_NUMBER = FrozenStyle(bg=pt.cv.GRAY_27, fg=pt.cv.GRAY_62, bold=True)
        self.PART_NEXT = FrozenStyle(fg=pt.cv.BLUE, bold=True)
        self.PART_PLAIN = FrozenStyle(fg=pt.cv.GRAY)
        self.PART_NEWLINE = FrozenStyle(fg=self.SEQ_CURSOR_FP.final.fg)
        self.PART_CARR_RET = self.PART_NEWLINE


class SequenceLegend:
    MAP = {
        Regex(R"\x1b\[0?m"): "reset SGR",
        Regex(R"\x1b\[([\d):;]+)m"): "regular SGR",
        Regex(R"\x1b\[(\d+)G"): "set cursor col.=%s",
        Regex(R"\x1b\[(\d+)d"): "set cursor line=%s",
        Regex(R"\x1b\[(\d+)F"): "cursor col.=1 ▲%s",
        Regex(R"\x1b\[(\d+)E"): "cursor col.=1 ▼%s",
        Regex(R"\x1b\[(\d+)A"): "mov cursor ▲%s",
        Regex(R"\x1b\[(\d+)B"): "mov cursor ▼%s",
        Regex(R"\x1b\[(\d+)C"): "mov cursor ▶%s",
        Regex(R"\x1b\[(\d+)D"): "mov cursor ◀%s",
        Regex(R"\x1b\[H"): "reset cursor",
        Regex(R"\x1b\[(\d*);?(\d*)H"): "set cursor %s,%s",
        Regex(R"\x1b7"): "save cursor pos",
        Regex(R"\x1b8"): "restore cursor pos",
        Regex(R"\x1b\[\?25l"): "hide cursor",
        Regex(R"\x1b\[\?25h"): "show cursor",
        Regex(R"\x1b\[0?J"): "clrscrn after cur",
        Regex(R"\x1b\[1J"): "clrscrn before cur",
        Regex(R"\x1b\[2J"): "clrscrn entirely",
        Regex(R"\x1b\[3J"): "clrscrn history",
        Regex(R"\x1b\[0?K"): "clrline after cur",
        Regex(R"\x1b\[1K"): "clrline before cur",
        Regex(R"\x1b\[2K"): "clrline entirely",
    }


@with_terminal_state  # @TODO send to stderr?
class action(_BaseAction):
    MANUAL_CONTROL_HINT = "Press any key to send next part of the data, or Ctrl+C to exit. "
    AUTO_CONTROL_HINT = "Press Ctrl+C to exit. "

    LEGEND_WIDTH = 24

    def __init__(
        self,
        termstate: ProxiedTerminalState,
        mode: EsqDbMode,
        merge: bool,
        delay: float,
        **kwargs,
    ):
        self._mode_manual_control = sys.stdin.isatty()
        self._mode_stats_display = sys.stdout.isatty()
        self._mode_merge_sgr = merge
        self._delay = delay
        self._styles = _Styles()

        if self._mode_manual_control:
            if mode is EsqDbMode.SEND:
                termstate.hide_cursor()
            termstate.disable_input()
        if self._mode_stats_display:
            termstate.assign_proxy(get_stderr())
            termstate.enable_alt_screen_buffer()
            get_stderr().echo(pt.make_reset_cursor())

        self._stream_types = {"out": "F", "in": "F"}
        self._last_seq_and_st = []

        self._run(mode, **kwargs)

    def _run(self, mode: EsqDbMode, infile: io.RawIOBase | None, outfile: io.IOBase):
        try:
            if mode is EsqDbMode.SEND:
                outfile = outfile or self._get_default_fifo(read=False)
                infile = infile or sys.stdin.buffer
                self._run_send(outfile, infile)
            elif mode is EsqDbMode.RECV:
                infile = infile or self._get_default_fifo(read=True)
                self._run_rcv(infile)
            else:
                raise RuntimeError(f"Invalid mode: {mode}")
        finally:
            if infile and not infile.closed:
                infile.close()
            if outfile and not outfile.closed:
                outfile.close()

    @cached_property
    def _split_regex(self) -> re.Pattern:
        if self._mode_merge_sgr:
            # splits by \e[0m as well
            # return re.compile(rb"(\x1b\[\??(?:[0-9;:]*[^0-9;:m]|0?m))")
            return re.compile(rb"(\x1b\[\??[0-9;:]*[^0-9;:m])")
        return re.compile(rb"(\x1b)")

    @staticmethod
    def _wrap_buffer(stream: io.RawIOBase) -> tuple[BinaryIO, int | None]:
        max_offset = None
        buf = stream
        if stream.seekable():
            stream.seek(0, os.SEEK_END)
            max_offset = stream.tell()
            stream.seek(0)
            buf = io.BufferedReader(stream)
        if isinstance(buf, io.TextIOWrapper):
            buf = buf.buffer
        return buf, max_offset

    @staticmethod
    def _get_default_fifo(read: bool) -> BinaryIO:
        stderr = get_stderr()
        default = ESQDB_DATA_PIPE
        if not os.path.exists(default):
            get_logger().debug(f"Creating FIFO: '{default}'")
            os.mkfifo(default, 0o600)

        stderr.echoi(('Destination', 'Source')[read]+" stream ")
        stderr.echo(f"is a NAMED PIPE:  '{default}'")
        if read:
            stderr.echo("Waiting for the sender to start transmitting.")
            return open(default, "rb")
        stderr.echo("Waiting for the receiver to connect.")
        return open(default, "wb")

    def _run_send(self, outfile: io.IOBase, infile: io.RawIOBase):
        stderr = get_stderr()
        logger = get_logger()
        get_logger().debug(f"SEND mode, {infile} -> {outfile}")

        if self._mode_stats_display:
            stderr.echo(pt.make_clear_display())
            stderr.echo(pt.make_move_cursor_down(9999))
        else:
            stderr.echo(
                "It seems like stderr stream is not connected to a terminal, "
                "so statistics are disabled."
            )
            if self._mode_manual_control:
                stderr.echo(self.MANUAL_CONTROL_HINT)
            else:
                stderr.echo(self.AUTO_CONTROL_HINT)

        buf_offset = 0
        inbuf, max_offset = self._wrap_buffer(infile)
        infname = getattr(infile, "name", "?")
        outfname = getattr(outfile, "name", "-")

        ps: deque[bytes] = deque()
        pll: int = 1
        offset: int = 0
        oll: int = 2 * math.ceil(len(f"{max_offset or 0:x}") / 2)
        idx: int = [-1, 0][self._mode_manual_control]

        letters = [
            self._get_fletter("in", infile),
            self._get_fletter("out", outfile),
            ("A", " ")[self._mode_manual_control],
            (" ", "M")[self._mode_merge_sgr],
        ]
        letters_str = " ".join(["", *letters, ""])

        while not inbuf.closed or len(ps):
            if not inbuf.closed and (len(ps) < 3 or buf_offset - offset < 1024):
                psp = inbuf.readline()
                if not len(psp):
                    inbuf.close()
                buf_offset += len(psp)
                pspl = re.split(self._split_regex, psp)
                while len(pspl):
                    p = pspl.pop(0)
                    if not len(ps) or re.search(rb"[^\x1b]", ps[-1]):
                        ps.append(p)
                    else:
                        ps[-1] += p
                pll = max(pll, len(str(len(ps))))

            if self._mode_stats_display:
                stderr.echoi(pt.make_set_cursor_column(1))
                stderr.echoi(pt.SeqIndex.RESET)
                stderr.echoi(pt.make_clear_line_after_cursor())

            twidth: int = get_terminal_width(pad=0)
            lineno = pt.Text(*self._format_part_no(idx - 1))
            olinew = max(1, twidth - len(lineno) - self.LEGEND_WIDTH)

            if len(ps) and idx > 0:
                p = ps.popleft()
                pw = p
                if pw == self.hide_cursor_seq:
                    pw = b""
                offset += outfile.write(pw)
                outfile.flush()

                oline = stderr.render(self._decode(p, partnum=idx - 1, preview=False) or "")
                olines = pt.wrap_sgr(oline, olinew).splitlines()
                for Lidx, o in enumerate(olines):
                    stderr.echoi_rendered(lineno)
                    if Lidx == 0:
                        lineno = pt.Text(*self._format_part_no(idx - 1, blank=True))
                    stderr.echoi(self._styles.PART_PLAIN.fg.to_sgr())
                    stderr.echoi(o)
                    while Lidx == 0 and self._last_seq_and_st:
                        seq, st = self._last_seq_and_st.pop(0)
                        if not seq:
                            continue
                        stderr.echoi(pt.SeqIndex.RESET)
                        stderr.echoi(pt.make_set_cursor_column(twidth - self.LEGEND_WIDTH + 1))
                        stderr.echoi_rendered(self._format_legend(seq, st, self.LEGEND_WIDTH - 2))

                    stderr.echo()

            if self._mode_stats_display:
                stderr.echoi(pt.make_move_cursor_down_to_start(1))

                left_st = self._styles.QUEUE
                stderr.echoi(left_st.bg.to_sgr(pt.ColorTarget.BG))
                stderr.echoi(pt.make_clear_line_after_cursor())
                if self._mode_manual_control and idx == -1:
                    stderr.echoi_rendered(self.MANUAL_CONTROL_HINT, left_st)
                    stderr.echoi(pt.make_set_cursor_column())

                else:
                    examplestr = self._decode(ps[0] if len(ps) else b"", partnum=idx, preview=True)

                    space_tx = (" ", self._styles.SBAR_BASE)
                    sep_tx = (" ", self._styles.SBAR_SEP_BASE)
                    max_offset_str = ["", f"/{max_offset!s:{oll}}"][bool(max_offset)]
                    status_right_fixed = pt.Text(
                        (sep_tx, space_tx),
                        (f"{idx:>{pll}d}", self._styles.CUR_PART_FMT),
                        (f"+{len(ps):>{pll}d}", self._styles.TOTAL_PARTS_FMT),
                        (space_tx, sep_tx, space_tx),
                        (f"{offset:{oll}d}", self._styles.CUR_PART_FMT),
                        (max_offset_str, self._styles.TOTAL_PARTS_FMT),
                        space_tx,
                    )

                    status_right_flex: pt.Text = pt.Text()
                    # if self._get_max_fname_len(twidth):
                    if fname_width := max(0, (twidth - len(status_right_fixed) - 16) // 2):
                        infname_str = pt.cut(infname, fname_width, ">")
                        outfname_str = pt.cut(outfname, fname_width, ">")

                        status_right_flex += (
                            (space_tx, infname_str, self._styles.TOTAL_PARTS_FMT),
                            (space_tx, "→", self._styles.CUR_PART_FMT),
                            (space_tx, outfname_str, self._styles.TOTAL_PARTS_FMT),
                        )

                    status_right_flex += (
                        (space_tx, sep_tx),
                        (letters_str, self._styles.LETTERS_FMT),
                        sep_tx,
                    )

                    if twidth < len(status_right_fixed):
                        status_right_flex = pt.Text()
                        status_right_fixed.set_width(min(twidth, len(status_right_fixed)))
                    else:
                        free = twidth - len(status_right_fixed)
                        status_right_flex.set_width(max(0, free))

                    if examplestr and (twidth - self.LEGEND_WIDTH) < len(examplestr):
                        examplestr.set_width(twidth - self.LEGEND_WIDTH)

                    stderr.echoi(left_st.bg.to_sgr(pt.ColorTarget.BG))
                    stderr.echoi(pt.make_clear_line_after_cursor())
                    examplestr.prepend(pt.Fragment("", left_st, close_this=False))
                    stderr.echoi_rendered((examplestr or ""))

                    stderr.echoi(pt.make_save_cursor_position())
                    stderr.echoi(pt.make_reset_cursor())
                    stderr.echoi(self._styles.SBAR_BG.to_sgr(pt.ColorTarget.BG))
                    stderr.echoi(pt.make_clear_line_after_cursor())
                    stderr.echoi_rendered(status_right_flex)
                    stderr.echoi_rendered(status_right_fixed)

                    stderr.echoi(pt.make_restore_cursor_position())

            self._wait(infile)

            logger.debug(f"State: (idx={idx}, offset={offset}/{max_offset})")
            if max_offset and offset == max_offset:
                if not self._mode_manual_control:
                    break
                stderr.echoi_rendered(
                    "Done. Press any key to exit",
                    FrozenStyle(bg=self._styles.SBAR_SEP_BG),
                )
                stderr.echoi(self._styles.SBAR_SEP_BG.to_sgr(pt.ColorTarget.BG))
                stderr.echoi(pt.make_clear_line_after_cursor())
                self._wait(infile)
                break

            idx += 1

    def _run_rcv(self, infile: io.RawIOBase):
        get_logger().debug(f"RECV mode, {infile} -> stdout")

        inbuf, max_offset = self._wrap_buffer(infile)
        if self._mode_stats_display:
            get_stdout().echoi(pt.make_clear_display())
            get_stdout().echoi(pt.make_reset_cursor())

        while i := inbuf.readline(1):
            get_stdout().io.buffer.write(i)  # noqa
            get_stdout().io.flush()

    hide_cursor_seq = pt.make_hide_cursor().assemble().encode()

    def _format_part_no(self, partnum: int, blank=False) -> Iterable[pt.RT]:
        yield pt.Fragment(f" {(str(partnum) if not blank else ''):4s} ", self._styles.PART_NUMBER)
        yield pt.Fragment("▏", FrozenStyle(self._styles.PART_NUMBER, bg=pt.DEFAULT_COLOR))

    @staticmethod
    def _format_legend(seq: pt.ISequence, st: SeqStyle, maxlen: int) -> pt.Fragment:
        seqass = seq.assemble()
        msg = repr(seq)
        for regex, desc in SequenceLegend.MAP.items():
            if m := regex.match(seqass):
                msg = desc
                if "%" in msg:
                    try:
                        msg %= m.groups()
                    except ValueError:
                        pass
                break
        return pt.Fragment(pt.fit(msg, maxlen, ">"), st.legend)

    def _decode(self, b: bytes, partnum: int, preview: bool) -> pt.Text:
        def _sanitize(s: str) -> str:
            return re.sub(
                r"(\x1b)|(\n+)|(\r+)|( +)",
                lambda m: (len(m[1] or "") * "ǝ")
                + (len(m[2] or "") * "↵\n")
                + (len(m[3] or "") * "⇤\r")
                + (len(m[4] or "") * "␣"),
                s,
            )

        result = pt.Text()
        ss = b.decode(errors="replace_with_qmark")
        for part in pt.parse(ss):
            if not result:
                if preview:
                    result.append(" NEXT ▏", self._styles.PART_NEXT)

            if not isinstance(part, pt.ISequence):
                for pline in re.split(r"(.[\n\r])", _sanitize(part)):
                    if pline.endswith("\n"):
                        result.append(pline.rstrip(), self._styles.PART_NEWLINE)
                    elif pline.endswith("\r"):
                        result.append(pline.rstrip(), self._styles.PART_CARR_RET)
                    else:
                        result.append(pline, self._styles.PART_PLAIN)
                continue

            seq = pt.ESCAPE_SEQ_REGEX.search(part.assemble())
            g = OrderedDict(
                {
                    k.rsplit("_", 1)[-1]: v
                    for k, v in seq.groupdict().items()
                    if v and re.match(r"data$|.+(_classifier|_interm|_param|_final)$", k)
                }
            )

            style = self._styles.SEQ_UNKNOWN
            if isinstance(part, pt.SequenceSGR):
                style = self._styles.SEQ_SGR
                if part == pt.SeqIndex.RESET:
                    style = self._styles.SEQ_SGR_RESET
            elif isinstance(part, pt.SequenceCSI):
                if g.get("final") in "HABDCFEdGn":
                    style = self._styles.SEQ_CURSOR
                elif g.get("final") in "JK":
                    style = self._styles.SEQ_ERASE
                elif g.get("final") in "lh" and g.get("interm") == "?":
                    style = self._styles.SEQ_PRIVATE
            elif isinstance(part, pt.SequenceFp):
                if g.get("classifier") in "78":
                    style = self._styles.SEQ_CURSOR_FP

            param = map(lambda p: (p, style.param), g.get("param", "").split(";"))
            params = pt.flatten1([*((p, (";", style.param_sep)) for p in param)])
            params.pop()
            result.append(
                "ǝ",
                style.escape_byte,
                g.get("classifier", ""),
                style.classifier,
                g.get("interm", ""),
                style.interm,
                *params,
                g.get("final"),
                style.final,
                " ",
            )
            if not preview:
                self._last_seq_and_st.append((part, style))
        return result

    def _wait(self, infile: io.IOBase):
        if self._mode_manual_control:
            pt.wait_key()
        else:
            time.sleep(self._delay)

    def _get_fletter(self, stype_key: str, file: io.IOBase) -> str:
        if file.isatty():
            return "T"
        elif getattr(file, "seekable", lambda: False)():
            return self._stream_types[stype_key]
        return "P"

    def _get_max_fname_len(self, twidth: int) -> int | None:
        if twidth < 60:
            return None
        return 10 + max(0, min((twidth - 80) // 5, 20))
