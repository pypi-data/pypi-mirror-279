# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import math
import os
import tempfile
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from functools import cached_property

import pytermor as pt
from es7s_commons import columns
from requests import Response

from es7s.shared import Styles as BaseStyles
from es7s.shared import (
    get_stdout,
    Requester,
    DataCollectionError,
    run_subprocess,
    is_x11,
)
from es7s.shared.enum import GraphOutputFormat
from ._base import _BaseAction


@dataclass(frozen=True)
class CoinloreTickerDTO:
    id: str
    symbol: str
    name: str
    nameid: str
    rank: int
    price_usd: str
    percent_change_24h: str
    percent_change_1h: str
    percent_change_7d: str
    price_btc: str
    market_cap_usd: str
    volume24: float
    volume24a: float
    csupply: float | None
    tsupply: float | None
    msupply: float | None

    @cached_property
    def market_cap_usd_f(self) -> float:
        return float(self.market_cap_usd)

    @cached_property
    def percent_change_24h_f(self) -> float:
        return float(self.percent_change_24h)


class Styles(BaseStyles):
    def __init__(self):
        self.CC_NAME = pt.FrozenStyle(bold=True)
        self.CC_PERC_CHANGE_COLORMAP = {
            1: pt.cv.GREEN,
            0: pt.cv.GRAY_50,
            -1: pt.cv.RED,
        }

    def get_perc_change_style(self, perc_change: float) -> pt.Style:
        sign = 0
        if perc_change:
            sign = int(perc_change / abs(perc_change))
        return pt.FrozenStyle(
            fg=self.CC_PERC_CHANGE_COLORMAP[sign],
            bold=True,
        )


class _AbstractFormatter(metaclass=ABCMeta):
    def __init__(self):
        self._styles = Styles()

    @abstractmethod
    def append(self, dtos: list[CoinloreTickerDTO]):
        ...

    @abstractmethod
    def format(self) -> str | pt.RT:
        ...

    @abstractmethod
    def write(self):
        ...


class action(_BaseAction):
    def __init__(self, **kwargs):
        self._styles = Styles()

        super().__init__(**kwargs)

        formatter_cls = FormatterFactory.get_formatter_class(**kwargs)
        self._run(formatter_cls)

    def _run(self, formatter_cls: type[_AbstractFormatter]):
        request = CoinloreTickersRequest()
        response = request.execute()
        data = response.json().get("data", [])
        dtos = [*request.deserialize(data)]
        formatter = formatter_cls()
        formatter.append(dtos)
        formatter.write()


class CliFormatter(_AbstractFormatter):
    def __init__(self):
        super().__init__()

        self._lines = []

    def append(self, dtos: list[CoinloreTickerDTO]):
        for dto in sorted(dtos, key=lambda d: -d.market_cap_usd_f):
            self._lines.append(self._format_dto(dto))

    def format(self) -> pt.RT:
        col, _ = columns(self._lines, gap=2)
        return col

    def write(self):
        get_stdout().echoi_rendered(self.format())

    def _format_dto(self, dto: CoinloreTickerDTO) -> pt.Text:
        result = pt.Text(
            pt.Fragment(dto.symbol, self._styles.CC_NAME),
            "\t",
        )

        perc_change_st = self._styles.get_perc_change_style(dto.percent_change_24h_f)
        perc_change_dim_st = pt.FrozenStyle(perc_change_st, dim=True, bold=False)
        perc_change_val = f"{dto.percent_change_24h_f:+6.2f}"
        result += pt.Fragment(perc_change_val, perc_change_st)
        result += pt.Fragment("%", perc_change_dim_st)

        return result


class DotFormatter(_AbstractFormatter):
    LAYOUT = "neato"
    TEMPLATE = f"""
graph {{
    layout={LAYOUT}
    pack=10
    node[shape=circle style=filled fontname="Munson"]
    
    %s
}}
"""

    def __init__(self):
        super().__init__()

        self._total_market_cap_usd = 0
        self._dtos = []

    def append(self, dtos: list[CoinloreTickerDTO]):
        for dto in dtos:
            self._total_market_cap_usd += dto.market_cap_usd_f
            self._dtos.append(dto)

    def format(self) -> str:
        nodes = []
        for dto in self._dtos:
            nodes.append(self._format_dto(dto))
        return self.TEMPLATE % ("\n" + pt.pad(4)).join(nodes)

    def write(self):
        get_stdout().echo(self.format())

    def _format_dto(self, dto: CoinloreTickerDTO) -> str:
        ratio = math.log10(1000 * dto.market_cap_usd_f / self._total_market_cap_usd)
        fontsize = 10 + 10 * ratio
        subfontsize = fontsize / 1.5

        change = abs(dto.percent_change_24h_f)
        peripheries = min(20, max(1, int(change // 2)))

        color_hue = 0
        if dto.percent_change_24h_f > 0:
            color_hue = 120
        fillcolor = pt.HSV(color_hue, 0.5, 0.95)
        bordercolor = pt.HSV(color_hue, 0.75, 0.75)

        label = (
            f"<<B>{dto.symbol}</B><BR/>"
            f'<FONT FACE="Arial" POINT-SIZE="{subfontsize}">'
            f"{dto.percent_change_24h_f:+.2f}%"
            f"</FONT>>"
        )

        return (
            f"{dto.symbol}["
            + " ".join(
                [
                    f"fontsize={fontsize}",
                    f"label={label}",
                    f"peripheries={peripheries}",
                    f"penwidth={min(2.0, max(0.5, change))}",
                    f'fillcolor="#{fillcolor.int:06X}"',
                    f'color="#{bordercolor.int:06X}"',
                ]
            )
            + f"]"
        )


class SvgFormatter(DotFormatter):
    def format(self) -> str:
        fd, name = tempfile.mkstemp(".dot", f"ccc{datetime.now().timestamp():.0f}", text=True)
        with os.fdopen(fd, "wt") as f:
            f.write(super().format())
        return name

    def write(self):
        dotfile = self.format()
        svgfile = f"{dotfile}.svg"
        run_subprocess(self.LAYOUT, "-Tsvg", f"-o{svgfile}", dotfile, check=True)

        if is_x11():
            run_subprocess("xdg-open", svgfile)
        else:
            with open(svgfile, "rt") as f:
                get_stdout().echo(f.read())

        os.unlink(dotfile)
        os.unlink(svgfile)


class FormatterFactory:
    CLASSMAP: dict[GraphOutputFormat, type[_AbstractFormatter]] = {
        GraphOutputFormat.CLI: CliFormatter,
        GraphOutputFormat.DOT: DotFormatter,
        GraphOutputFormat.SVG: SvgFormatter,
        GraphOutputFormat.PNG: SvgFormatter,
    }

    @classmethod
    def get_formatter_class(cls, format: GraphOutputFormat) -> type[_AbstractFormatter]:
        if format not in cls.CLASSMAP.keys():
            raise KeyError(f"No formatter class defined for format: {format!r}")
        return cls.CLASSMAP.get(format)


class CoinloreTickersRequest:
    URL = "https://api.coinlore.net/api/tickers/"

    def __init__(self):
        self._requester = Requester()

    def execute(self) -> Response:
        try:
            response: Response = self._requester.make_request(url=self.URL)
        except DataCollectionError as e:
            raise e
        return response

    def deserialize(self, data: dict) -> Iterable[CoinloreTickerDTO]:
        for dto in data:
            yield CoinloreTickerDTO(**dto)
