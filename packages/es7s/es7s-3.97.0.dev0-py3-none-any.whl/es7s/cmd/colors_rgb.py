# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

from collections.abc import Iterable

import pytermor as pt

from es7s.cmd._base import _BaseAction
from es7s.shared import get_stdout


class action(_BaseAction):
    def __init__(self, **kwargs):
        self._run(**kwargs)

    def _run(self, invert: bool, width: int):

        def inv(*vv: int) -> Iterable[int]:
            yield from [255 - v for v in vv]

        s = " ·" * (width // 2 + 1)
        colors = []

        stdout = get_stdout()
        stdout.echo(pt.SeqIndex.BOLD)

        for c in range(width):
            r = 255 - (c * 255 // (width - 1))
            g = c * 510 // (width - 1)
            b = c * 255 // (width - 1)
            if g > 255:
                g = 510 - g
            if invert:
                r, g, b = inv(r, g, b)
            colors.append((r, g, b, s[c]))

        for col in [*colors]:
            if not col:
                stdout.echo()
                continue
            r, g, b, c = col
            stdout.echo_rendered(
                pt.Fragment(
                    c,
                    pt.Style(
                        # fg=pt.rgb_to_hex(pt.RGB(max(0, r - 128), max(0, g - 128), max(0, b - 128))),
                        fg=pt.ColorRGB(pt.RGB.from_channels(255 - r, 255 - g, 255 - b)),
                        bg=pt.ColorRGB(pt.RGB.from_channels(r, g, b)),
                    ),
                ),
                nl=False,
            )
        stdout.echo(pt.SeqIndex.BOLD_DIM_OFF)
        stdout.echo()
