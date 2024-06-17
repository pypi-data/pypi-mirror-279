# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import abc
import os
import random
import re
import subprocess
import sys
from abc import abstractmethod
from collections import OrderedDict
from collections.abc import Iterable
from dataclasses import dataclass
from subprocess import CompletedProcess
from typing import Dict

import pytermor as pt
from es7s_commons import columns
from pytermor import SequenceSGR, NOOP_SEQ

from ._base import _BaseAction
from ..shared import get_stdout, get_logger


class Keyword:
    def __init__(self, name: str):
        self._name = name

    def __str__(self):
        return ""

    def __repr__(self):
        return f"{self._name}"


@dataclass(frozen=True)
class EntryType:
    sorter: int
    centered: bool = False
    template: str = "%s"

    def format(self, k: str) -> str:
        try:
            return self.template % k
        except ValueError as e:
            get_logger().non_fatal_exception(e)
            return k


class EntryTypeRegistry:
    SPECIAL = EntryType(10, True, "[%s]")
    EXTENSION = EntryType(20)
    CAPS = EntryType(30, True)
    UNKNOWN = EntryType(100)

    @classmethod
    def classify(cls, val: str) -> EntryType:
        if len(val) == 2:
            return cls.SPECIAL
        if val.startswith("*."):
            return cls.EXTENSION
        if val.isupper():
            return cls.CAPS
        return cls.UNKNOWN


class Sorter(metaclass=abc.ABCMeta):
    @classmethod
    @abstractmethod
    def sort(cls, kv: tuple[str, SequenceSGR | Keyword]) -> tuple[str | int | None, ...]:
        ...


class SorterByColor(Sorter):
    COLORS_16 = {*pt.ALL_COLORS} - {pt.IntCode.COLOR_EXTENDED, pt.IntCode.BG_COLOR_EXTENDED}

    @classmethod
    def sort(cls, kv) -> tuple[str | int | None, ...]:
        k, v = kv
        prefix = -1
        if isinstance(v, Keyword):
            return (prefix,)
        if len(v.params) > 0:
            if v.params[0] in cls.COLORS_16:
                prefix = v.params[0] % 10
            else:
                prefix = 10
        return prefix, *v.params, *SorterByValue.sort(kv)


class SorterByValue(Sorter):
    @classmethod
    def sort(cls, kv) -> tuple[str | int | None, ...]:
        k, _ = kv
        return EntryTypeRegistry.classify(k).sorter, re.sub(r"[^a-z0-9.]+", "", k.lower())


class Formatter(metaclass=abc.ABCMeta):
    RESET_ALL_BUT_FG = "\x1b[22;23;24;27;49m"

    def __init__(self, key_len: int):
        self._key_len = key_len

    @abstractmethod
    def format(self, ds: Dataset) -> str:
        ...


class FormatterShort(Formatter):
    def format(self, ds: Dataset) -> Iterable[str]:
        for (val, fmt) in ds.items():
            et = EntryTypeRegistry.classify(val)
            align = (pt.Align.LEFT, pt.Align.CENTER)[et.centered]
            valstr = pt.fit(et.format(val), self._key_len, align)

            yield f"{fmt}{valstr}{self.RESET_ALL_BUT_FG}{pt.SeqIndex.RESET}"


class FormatterExtended(Formatter):
    def _format_params(self, fmt: SequenceSGR) -> str:
        if not isinstance(fmt, SequenceSGR):
            return repr(fmt)
        return " ".join(map(str, fmt.params)) or "noop"

    def format(self, ds: Dataset) -> Iterable[str]:
        params_width = max(len(self._format_params(fmt)) for fmt in ds.values())
        for (val, fmt) in ds.items():
            et = EntryTypeRegistry.classify(val)
            align = pt.Align.RIGHT
            valstr = pt.fit(et.format(val), self._key_len, align)
            _, p, v = re.split(R"(^\s*)", valstr)
            valfmtd = (f"{p}{fmt}{v}", f"{fmt}{p}{v}")[et == EntryTypeRegistry.SPECIAL]

            yield f"{valfmtd}{pt.SeqIndex.RESET}  {self._format_params(fmt):<{params_width}s}"


Dataset = Dict[str, SequenceSGR|Keyword]


class action(_BaseAction):
    ENV_VARNAME = "LS_COLORS"
    KEYWORDS = {
        "target": Keyword("target"),
    }

    def __init__(self, *args, extend: bool, sort_by_color: bool, rows_first: bool, **kwargs):
        self._extend = extend
        self._rows_first = rows_first
        self._sort_by_color = sort_by_color
        self._run()

    def _run(self):
        random.seed(0)
        raw = self._get_raw_value()
        parsed = self._parse_raw_value(raw)
        sorted = self._sort(parsed)
        self._print(sorted)

    def _get_raw_value(self) -> str:
        if raw := self._read_env_directly():
            return raw
        if raw := self._extract_env_from_shell():
            return raw
        raise RuntimeError(f"Failed to get {self.ENV_VARNAME} value")

    def _read_env_directly(self) -> str | None:
        return os.getenv(self.ENV_VARNAME, None)

    def _extract_env_from_shell(self) -> str | None:
        p: CompletedProcess = subprocess.run(
            ["bash", "-i", "-c", "env"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf8",
            check=True,
        )
        for line in p.stdout.splitlines():
            if match := re.fullmatch(f"^{self.ENV_VARNAME}=(.+)$", line):
                return match.group(1)
        return None

    def _parse_raw_value(self, raw: str) -> Dataset:
        result = dict()
        for setting in raw.split(":"):
            if "=" not in setting:
                continue
            k, _, v = setting.strip().partition("=")

            result[k] = NOOP_SEQ
            if v not in ["", "0"]:
                if v in self.KEYWORDS.keys():
                    result[k] = self.KEYWORDS.get(v, None)
                    continue
                try:
                    result[k] = SequenceSGR(*(int(p) for p in v.split(";")))
                except ValueError:
                    print(f'WARNING: not a valid SGR param: "{v}" in: {setting}', file=sys.stderr)
                    result[k] = NOOP_SEQ
        return result

    @property
    def _sorter(self) -> type[Sorter]:
        return (SorterByValue, SorterByColor)[self._sort_by_color]

    @property
    def _formatter(self) -> type[Formatter]:
        return (FormatterShort, FormatterExtended)[self._extend]

    def _sort(
        self, parsed: Dataset
    ) -> Dataset:
        return OrderedDict({k: v for (k, v) in sorted(parsed.items(), key=self._sorter.sort)})

    def _print(self, sorted: Dataset):
        key_len = max(len(k) for k in sorted.keys())
        if not self._extend:
            key_len = min(key_len, 7)

        fmter: Formatter = self._formatter(key_len)
        results = [*fmter.format(sorted)]
        result_str, _ = columns(results, gap=1, rows_first=self._rows_first)
        get_stdout().echo(result_str)
