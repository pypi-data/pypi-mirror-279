# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re
from collections import Counter
from itertools import product
from math import floor
from pathlib import Path

import pytermor as pt
from es7s_commons import Regex
from es7s_commons import Scale

from ._adaptive_input import _AdaptiveInputAction
from ._base import _BaseAction
from ..cli._base import NWMarkup
from ..shared import get_stdout, Styles as BaseStyles, get_demo_res, get_stderr

from ..shared.cp_char_freq import (
    EncodingPair,
    EncodingStats,
    Encoding,
    ENCODINGS_MOST_FREQ_CHARS,
    MOST_FREQ_CHAR_MAP,
)

CYRILLIC_RATIO_THRESHOLD = 0.50


UNICODE_CONTROL_CHARS = [*pt.char_range("\u0080", "\u009f")]


class NonPrintsStringRefilter(NWMarkup.RenderingNamedGroupsRefilter):
    def __init__(self):

        super().__init__(
            Regex(
                R"""
					(?P<spc>␣+)|
					(?P<cyr>[А-ЯЁ]+)|
					(?P<cyrs>[а-яё]+)|
					(?P<lat>[A-Za-z0-9]+)|
					(?P<psg>[\u2500-\u256f]+)|
					(?P<blk>[\u2580-\u259f]+)|
					(?P<acc>▯+)
				""",
                verbose=True,
            ),
            {
                "spc": pt.cv.CYAN,
                "cyr": pt.cv.HI_GREEN,
                "cyrs": pt.cv.GREEN,
                "lat": pt.cv.HI_GREEN,
                "psg": pt.cv.BLUE,
                "blk": pt.cv.YELLOW,
                "acc": pt.cv.HI_RED,
            },
        )


class NonPrintsStringVisualizer(pt.StringMapper):
    def __init__(self):
        override = {
            0x0A: "↵",
            0x20: "␣",
        }
        super().__init__(override)

    def _get_default_keys(self) -> list[int]:
        return (
            pt.WHITESPACE_CHARS
            + pt.CONTROL_CHARS
            + [*map(ord, UNICODE_CONTROL_CHARS)]
            + [0xAD, 0xA0]
        )

    def _get_default_replacer(self) -> str:
        return "▯"


class action(_AdaptiveInputAction, _BaseAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._vis = [NonPrintsStringVisualizer(), NonPrintsStringRefilter()]
        self._run(**kwargs)

    def _get_demo_input(self) -> Path | None:
        return get_demo_res("demo-groboscope.txt")

    def _run(self, stats: bool, build: bool, full: bool, **kwargs):
        if stats:
            self._print_frequencies()
            return

        input_data = "\n".join(self._input_lines)
        # input_data = re.sub(R" +", "", input_data)
        if build:
            self._build_frequencies(input_data)
        else:
            if not input_data.strip():
                self._exit_with_empty_input_msg()
            encpairs = self._analyze_input(input_data)
            self._attempt_to_reencode(input_data, encpairs, full)

    def _build_frequencies(self, input_data: str):
        stdout = get_stdout()
        stderr = get_stderr()

        frequencies = dict[EncodingPair, Counter]()
        for (cfrom, cto) in product(Encoding, Encoding):
            encpair = EncodingPair((cfrom, cto))
            if not Encoding.is_allowed(cfrom, cto):
                continue
            try:
                encoded = input_data.encode(cfrom.value.label)
                decoded = encoded.decode(cto.value.label, errors="replace")
            except Exception as e:
                stderr.echoi(encpair.generate_code())
                stderr.echo_rendered("FAIL: " + str(e), BaseStyles.ERROR)
                continue
            frequencies[encpair] = Counter(decoded)

        most_freq_char_map = dict[str, list[EncodingStats]]()
        for encpair, counter in frequencies.items():
            for (ch, freq) in counter.most_common():
                if ch not in most_freq_char_map.keys():
                    most_freq_char_map[ch] = []
                most_freq_char_map[ch].append(EncodingStats(encpair, ch, freq))
        for ch in most_freq_char_map.keys():
            most_freq_char_map[ch].sort(key=lambda ef: ef.freq)

        stdout.echo("ENCODINGS_MOST_FREQ_CHARS = {")
        for (encpair, counter) in frequencies.items():
            record = f"    {encpair.generate_code()}: ["
            for (char, count) in counter.most_common(16):
                record += f'("\\u{ord(char):04x}", {100*count/counter.total():6.3f}), '
            record += "], "
            get_stdout().echo(record)
        stdout.echo("}")

        stdout.echo("MOST_FREQ_CHAR_MAP = {")
        for (char, stats) in most_freq_char_map.items():
            record = f'    "\\u{ord(char):04x}": ['
            record += ", \n".join(stat.encpair.generate_code() for stat in stats)
            record += "],"
            get_stdout().echo(record)
        stdout.echo("}")

    def _analyze_input(self, input_data: str) -> Counter[EncodingPair]:
        stderr = get_stderr()

        stats = Counter[str](input_data)
        stderr.echo_rendered("Most frequent code points:", BaseStyles.TEXT_DEFAULT)
        for char, val in stats.most_common()[:6]:
            stderr.echoi_rendered(self._format_char_freq(char, 100 * val / stats.total()))
        stderr.echo()
        stderr.echo()

        encpairs = Counter[EncodingPair]()
        for char, count in stats.most_common():
            for encoding_suggestion in MOST_FREQ_CHAR_MAP.get(char, []):
                encpair = EncodingPair(encoding_suggestion)
                encpairs[encpair] += 1

        header = pt.Text("Most probable operations: ", BaseStyles.TEXT_DEFAULT)

        ENCPAIRS_DISPLAY_LIMIT = 5
        if (encpairs_hidden := len(encpairs) - ENCPAIRS_DISPLAY_LIMIT) > 0:
            header += (f" (+{encpairs_hidden} not shown)", BaseStyles.TEXT_LABEL)
        stderr.echo_rendered(header)

        for (enc, count) in encpairs.most_common()[:ENCPAIRS_DISPLAY_LIMIT]:
            scale = Scale(
                count / encpairs.total(),
                pt.NOOP_STYLE,
                pt.Style(bold=True, bg=pt.cv.BLACK),
            )
            stderr.echoi_rendered(enc.format())
            stderr.echo_rendered(scale)
        stderr.echo()

        return encpairs

    def _attempt_to_reencode(self, input_data: str, encpairs: Counter[EncodingPair], full: bool):
        stdout = get_stdout()
        stderr = get_stderr()
        attempts = 0

        stderr.echo_rendered(
            pt.Text(
                f"Attempting to reencode: ",
                BaseStyles.TEXT_DEFAULT,
                " (pass '-f' if full result is required)",
                BaseStyles.TEXT_LABEL,
            )
        )
        for (encpair, _) in encpairs.most_common():
            cfrom, cto = encpair
            attempts += 1
            if not Encoding.is_allowed(cfrom, cto):
                continue
            stderr.echoi_rendered(EncodingPair(encpair).format(reverse=True))

            encoding_errors = False
            decoding_errors = False
            try:
                try:
                    encoded = input_data.encode(cto.value.label)
                except Exception:
                    encoding_errors = True
                    encoded = input_data.encode(cto.value.label, errors="replace")

                try:
                    decoded = encoded.decode(cfrom.value.label)
                except Exception:
                    decoding_errors = True
                    decoded = encoded.decode(cfrom.value.label, errors="replace")

            except Exception as e:
                stderr.echo_rendered(
                    pt.Text(
                        "X",
                        pt.Style(bold=True, bg="red", fg="gray0"),
                        " ",
                        str(e),
                        BaseStyles.MSG_FAILURE_DETAILS,
                    )
                )
                continue

            cyrillic = sum(map(len, re.findall(R"[А-ЯЁа-яё]+", decoded))) / len(decoded)
            cyr_st = BaseStyles.TEXT_LABEL
            example_st = BaseStyles.TEXT_DISABLED
            if cyrillic > CYRILLIC_RATIO_THRESHOLD:
                if encoding_errors:
                    cyr_st = BaseStyles.WARNING_LABEL
                else:
                    cyr_st = BaseStyles.MSG_SUCCESS
                    example_st = pt.cvr.AIR_SUPERIORITY_BLUE

            status = pt.Text()
            if not encoding_errors and not decoding_errors:
                status += ("+", pt.Style(fg="gray0", bold=True, bg="green"))
            else:
                status_warn = ""
                if encoding_errors and decoding_errors:
                    status_warn = "!"
                elif encoding_errors:
                    status_warn = "E"
                elif decoding_errors:
                    status_warn = "D"
                status += (status_warn, pt.Style(fg="gray0", bold=True, bg="yellow"))
            status += (
                " ",
                f"{100*cyrillic:5.1f}% cyrillic  ",
                cyr_st,
            )

            stderr.echoi_rendered(status)
            if full:
                stderr.echo_rendered(f"({len(decoded)} chars » stdout)", BaseStyles.TEXT_LABEL)
                stdout.echo(decoded)
            else:
                stderr.echo_rendered(
                    pt.apply_filters(pt.cut(decoded, 80), self._vis[0]), example_st
                )

    def _print_frequencies(self):
        stderr = get_stderr()
        VSEP = "  "

        termw = pt.get_terminal_width(pad=0)
        CWIDTH = min(
            floor((termw - 16 - len(VSEP)) / (1 + len(Encoding))) - 1,
            min(map(len, ENCODINGS_MOST_FREQ_CHARS.values())),
        )
        FNUM = floor((termw - 2 * CWIDTH - len(VSEP)) / (1 + len(self._format_char_freq(".", 0))))

        for (encpair, most_common) in ENCODINGS_MOST_FREQ_CHARS.items():
            label = encpair[0].format(CWIDTH, ">") + " → " + encpair[1].format(CWIDTH, "<") + VSEP
            stderr.echoi_rendered(label)

            for char, val in most_common[:FNUM]:
                stderr.echoi_rendered(self._format_char_freq(char, val))
            stderr.echo()

        stderr.echo()
        stderr.echo("-" * min(125, pt.get_terminal_width(pad=0)))
        stderr.echo()

        stderr.echoi(pt.pad(CWIDTH) + VSEP)
        for cto in Encoding:
            # if not Encoding.is_allowed(None, cto):
            #     continue
            stderr.echoi_rendered("→ " + cto.format(CWIDTH - 2, "<") + VSEP)
        stderr.echo()
        stderr.echo()

        for cfrom in Encoding:
            # if not Encoding.is_allowed(cfrom):
            #     continue
            stderr.echoi_rendered(cfrom.format(CWIDTH - 2, ">") + " →" + VSEP)
            for cto in Encoding:
                # if not Encoding.is_allowed(cfrom, cto):
                #     continue
                result = ENCODINGS_MOST_FREQ_CHARS.get((cfrom, cto), None)
                value = pt.Fragment("░" * (CWIDTH), pt.cv.GRAY_42)
                if result is None:
                    pass
                elif isinstance(result, Exception):
                    pass
                elif isinstance(result, list):
                    value = "".join([pt.apply_filters(k, *self._vis) for k, _ in result[:CWIDTH]])
                else:
                    raise RuntimeError(type(result))
                stderr.echoi_rendered(value + VSEP)
            stderr.echo()

    def _format_char_freq(self, char: str, val: float) -> pt.Text:
        return pt.Text(
            f" {val:>2.0f}% ",
            BaseStyles.TEXT_DEFAULT,
            pt.apply_filters(char, *self._vis),
            BaseStyles.TEXT_SUBTITLE,
            f" U+{ord(char):04X} ",
            BaseStyles.TEXT_LABEL,
            "  ",
        )
