# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re
import textwrap

import pytermor as pt

from ._base import _BaseAction
from ..shared import run_subprocess, get_stdout, Styles as BaseStyles
from ..shared.enum import PrintFfmpegMode


class Styles(BaseStyles):
    def __init__(self, mode: PrintFfmpegMode):
        self.EMPTY_CHAR_ORIGIN = "."
        self.EMPTY_CHAR_CURRENT = "-"
        FMT_CODEC_TYPE = pt.Style(bold=True)

        self.ST_DECODER = pt.cv.GREEN
        self.ST_ENCODER = pt.cv.RED
        self.ST_VIDEO = pt.Style(FMT_CODEC_TYPE, fg=pt.cv.BLUE)
        self.ST_AUDIO = pt.Style(FMT_CODEC_TYPE, fg=pt.cv.YELLOW)
        self.ST_SUBTITLES = pt.Style(FMT_CODEC_TYPE, fg=pt.cv.HI_WHITE)
        self.ST_MISC_TYPE = self.TEXT_LABEL
        self.ST_LOSSY = pt.cv.HI_CYAN
        self.ST_LOSELESS = pt.cv.HI_MAGENTA
        self.ST_EXPERIMENTAL = pt.FrozenStyle(bg=pt.cv.HI_YELLOW, fg=pt.cv.GRAY_0)

        match (mode):
            case PrintFfmpegMode.DECODERS:
                self.ST_CODEC = self.ST_DECODER
            case PrintFfmpegMode.ENCODERS:
                self.ST_CODEC = self.ST_ENCODER
            case _:
                self.ST_CODEC = pt.NOOP_STYLE

        def __from_default(kv: dict) -> dict:
            d = FMT_DEFAULT.copy()
            d.update(**kv)
            return d

        FMT_DEFAULT = {
            "V": self.ST_VIDEO,
            "A": self.ST_AUDIO,
            self.EMPTY_CHAR_ORIGIN: self.TEXT_DISABLED,
        }

        if mode is PrintFfmpegMode.CODECS:
            self._FMT_MAP = __from_default(
                {
                    "D": [self.ST_DECODER, None, self.ST_MISC_TYPE],
                    "E": self.ST_ENCODER,
                    "S": [None, None, self.ST_SUBTITLES, None, None, self.ST_LOSELESS],
                    "L": self.ST_LOSSY,
                    "I": self.TEXT_DEFAULT,
                }
            )
        else:
            self._FMT_MAP = __from_default(
                {
                    "F": self.TEXT_DEFAULT,
                    "S": [self.ST_SUBTITLES, None, self.TEXT_DEFAULT],
                    "X": self.ST_EXPERIMENTAL,
                    "B": self.TEXT_DEFAULT,
                    "D": self.TEXT_DEFAULT,
                }
            )

    def get_fmt(self, chr: str, idx: int = 0) -> pt.FT:
        st = self._FMT_MAP.get(chr, pt.NOOP_STYLE)
        if isinstance(st, list):
            if idx < len(st):
                return st[idx] or pt.NOOP_STYLE
            return st[-1]
        return st

    def get_codec_st(self, match: str) -> pt.FT:
        if match.startswith("(de"):
            return self.ST_DECODER
        elif match.startswith("(en"):
            return self.ST_ENCODER
        elif match.startswith("(co"):
            return self.ST_CODEC
        return pt.NOOP_STYLE


class action(_BaseAction):
    def __init__(self, mode: PrintFfmpegMode):
        self._styles = Styles(mode)
        self._run(mode)

    def _run(self, mode: PrintFfmpegMode):

        try:
            cp = run_subprocess("ffmpeg", f"-{mode}")
        except FileNotFoundError as e:
            raise RuntimeError("Executable ffmpeg is not available") from e

        lines = []
        max_name_len = 0
        flags_length = len(self._fmt())
        prev_flag_type = None
        flag_type_idx = [0, 2][mode is PrintFfmpegMode.CODECS]

        for line in cp.stdout.splitlines():
            if re.match(R"^\s", line):
                parts = re.split(R"\s+", line.strip(), maxsplit=2)
                flags = parts.pop(0).strip()
                if parts:
                    if (
                        not parts[0].strip().startswith("=")
                        and prev_flag_type != flags[flag_type_idx]
                    ):
                        if prev_flag_type:
                            lines.append("")
                        prev_flag_type = flags[flag_type_idx]
                    max_name_len = max(max_name_len, len(parts[0]))
                else:
                    lines.append("")
                    continue
                flags_tx = self._fmt(flags)
                lines.append((flags_tx, *parts))

        max_name_len += 2
        desc_offset = flags_length + max_name_len
        for line in lines:
            if isinstance(line, str):
                get_stdout().echo(line)
                continue
            if isinstance(line, tuple) and len(line) == 1:
                get_stdout().echo(*line)
                continue
            flags, name, desc = line

            get_stdout().echoi_rendered(flags)
            get_stdout().echoi_rendered(pt.fit(name, max_name_len), self._styles.TEXT_SUBTITLE)

            desc = "\n".join(
                textwrap.wrap(
                    (self._styles.EMPTY_CHAR_CURRENT * desc_offset) + desc,
                    width=pt.get_terminal_width(),
                    subsequent_indent=pt.pad(desc_offset),
                )
            )

            desc = re.sub(
                R"(\((?:en|de)?code[rc]s?:?\s*)(.+?)\s*(\))",
                lambda m: get_stdout().render(
                    pt.Text(
                        (m.group(1), self._styles.TEXT_LABEL),
                        (m.group(2), self._styles.get_codec_st(m.group(1))),
                        (m.group(3), self._styles.TEXT_LABEL),
                    )
                ),
                desc,
                flags=re.DOTALL,
            )
            get_stdout().echo(desc[desc_offset:])

    def _fmt(self, flags: str = None) -> pt.Text:
        ss = pt.Text(pt.pad(1))
        for idx, c in enumerate(flags or self._styles.EMPTY_CHAR_CURRENT * 6):
            st = self._styles.get_fmt(c, idx)
            if c == self._styles.EMPTY_CHAR_ORIGIN:
                c = self._styles.EMPTY_CHAR_CURRENT
            ss += pt.Fragment(c, st)
        ss += pt.pad(2)
        return ss
