from __future__ import annotations

import abc
import enum
import math
import os
import typing as t
from abc import abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from itertools import product
from sys import maxunicode
from typing import ClassVar

import click
import pytermor as pt

from es7s.shared import FrozenStyle


class OptAuto(int):
    def __int__(self):
        return 0

    def __str__(self):
        return "auto"


OPT_VALUE_AUTO = OptAuto()


# -----------------------------------------------------------------------------
# Parameter types


class IntRange(click.IntRange):
    """
    ...
    """

    def __init__(
        self,
        _min: int = None,
        _max: int = None,
        min_open: bool = False,
        max_open: bool = False,
        clamp: bool = False,
        show_range: bool = True,
    ):
        self._show_range = show_range
        super().__init__(_min, _max, min_open, max_open, clamp)

    def get_metavar(self, param: click.Parameter = None) -> t.Optional[str]:
        return "N"

    def _describe_range(self) -> str:
        if not self._show_range:
            return ""
        return super()._describe_range().replace("x", self.get_metavar())


class CharIntRange(click.IntRange):
    def __init__(self):
        super().__init__(min=0, max=maxunicode, clamp=False)

    def convert(self, value, param, ctx) -> int:
        if isinstance(value, str) and value.startswith("0x"):
            return int(value, 16)
        return super().convert(value, param, ctx)


class FloatRange(click.FloatRange):
    def __init__(
        self,
        _min: float = None,
        _max: float = None,
        min_open: bool = False,
        max_open: bool = False,
        clamp: bool = False,
        show_range: bool = True,
    ):
        self._show_range = show_range
        self._range_filters = [
            pt.StringReplacer("x", lambda _: self.get_metavar()),
            pt.StringReplacer("inf", "∞"),
        ]
        super().__init__(_min, _max, min_open, max_open, clamp)

    def get_metavar(self, param: click.Parameter = None) -> t.Optional[str]:
        return "X"

    def _describe_range(self) -> str:
        if not self._show_range:
            return ""
        return pt.apply_filters(super()._describe_range(), *self._range_filters)


class EnumChoice(click.Choice):
    """
    Note: `show_choices` is ignored if param has custom metavar. That's because
    both metavar and choices in the left column of parameter list in --help mode
    look like shit and mess up the whole table. In case you need to set a metavar
    and to display choices at the same, add the latter into "help" message
    by setting `inline_choices` to True.
    """

    def __init__(self, impl: t.Any | enum.Enum, show_choices: bool = None, inline_choices=False):
        self.__impl = impl
        self._show_choices: bool | None = show_choices
        self.inline_choices = inline_choices
        super().__init__(choices=[item.value for item in impl], case_sensitive=False)

    def get_metavar(self, param: click.Parameter) -> str:
        if isinstance(param, click.Argument) and self._show_choices is not True:
            return param.name.upper()
        if self._show_choices is True:
            return super().get_metavar(param)
        return ""

    def get_choices_str(self) -> str:
        return " [" + "|".join(iter(self.__impl)) + "]"

    def convert(self, value, param, ctx):
        if value is None or isinstance(value, enum.Enum):
            return value

        converted_str = super().convert(value, param, ctx)
        return self.__impl(converted_str)


class IpParamType(click.ParamType):
    name = "ip"

    def convert(
        self,
        value: t.Any,
        param: t.Optional[click.Parameter],
        ctx: t.Optional[click.Context],
    ) -> t.Any:
        import ipaddress

        if not value:
            return None

        try:
            return ipaddress.ip_address(value)
        except ValueError:
            self.fail(f"{value!r} is not a valid IP.", param, ctx)

    def __repr__(self) -> str:
        return "IP"


class DateTimeType(click.DateTime, metaclass=abc.ABCMeta):
    metavar: str = None
    default_help: str = None
    format_section: t.Iterable[HelpPart] = None

    def __init__(self):
        super().__init__([*self.get_formats()])

    @staticmethod
    @abstractmethod
    def get_formats() -> Iterable[str]:
        ...

    @classmethod
    def format_supported_formats(cls) -> str:
        examples = []
        max_f, max_ex = 0, 0
        for f in cls.get_formats():
            ex = datetime.today().strftime(f)
            max_f, max_ex = max(max_f, len(f)), max(max_ex, len(ex))
            examples.append((f, ex))

        results = []
        for f, ex in examples:
            result = f"{f:<{max_f}s} ({ex})".ljust(max_f + max_ex + 3)
            results.append(result.replace(" ", "\u00a0"))

        return "   ".join(results)


# -----------------------------------------------------------------------------
# Command options


class ScopedOption(click.Option, metaclass=abc.ABCMeta):
    envvar_support = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.envvar_support:
            cli_debug = bool(os.getenv("ES7S_CLI_ENVVAR"))
            self.show_envvar = cli_debug
            self.allow_from_autoenv = cli_debug

    @property
    @abstractmethod
    def scope(self) -> OptionScope:
        raise NotImplementedError

    def has_argument(self):
        if isinstance(self.type, click.IntRange):
            return not self.count
        return isinstance(
            self.type,
            (
                click.FloatRange,
                click.Choice,
                click.DateTime,
            ),
        )


class OptionScope(str, enum.Enum):
    COMMON = "Common options"
    GROUP = "Group options"
    COMMAND = "Options"

    def __str__(self):
        return self.value


class CommonOption(ScopedOption):
    scope = OptionScope.COMMON


class GroupOption(ScopedOption):
    scope = OptionScope.GROUP
    envvar_support = True


class CommandOption(ScopedOption):
    scope = OptionScope.COMMAND
    envvar_support = True


class SharedOptions:
    def __init__(self, items: list[click.Parameter], help: list[HelpPart] = None):
        self._items = items
        self._help: list[HelpPart] | None = help

    @property
    def items(self) -> list[click.Parameter]:
        return self._items

    @property
    def help(self) -> list[HelpPart]:
        return self._help


# -----------------------------------------------------------------------------
# Command description


@dataclass(frozen=True)
class Section:
    title: str
    content: t.Sequence[pt.RT | t.Iterable[pt.RT]]

    def __bool__(self) -> bool:
        return len(self.content) > 0


@dataclass()
class HelpPart:
    """
    :param width_ratio: in (0.00; 1.00] range
    """

    text: str | list[tuple[pt.RT, pt.RT]]
    title: str = None
    group: str | int = None
    indent_shift: int = 0
    width_ratio: float = None


EPILOG_COMMAND_HELP = HelpPart(
    "Run 'es7s%s' COMMAND '--help' to get the COMMAND usage details (e.g. 'es7s%s %s --help').",
    group="run",
)
EPILOG_COMMON_OPTIONS = HelpPart(
    "Run 'es7s help options' to see common options details ('-v', '-Q', '-c', '-C', '--tmux', "
    "'--default').",
    group="run",
)
EPILOG_COMMANDS_TREE = HelpPart(
    "Run 'es7s help commands' to see full command tree and legend for command types.",
    group="run",
)
EPILOG_ARGS_NOTE = HelpPart(
    "Mandatory or optional arguments to long options are also mandatory or optional for any "
    "corresponding short options."
)


class DayMonthType(DateTimeType):
    metavar = "DD-MM"
    default_help = "Date of interest, see *Date* *format* section."

    @staticmethod
    def get_formats() -> Iterable[str]:
        return ["%b-%d", "%m-%d", "%d-%b", "%m-%b", "%b%d", "%m%d", "%d%b", "%d%m"]

    @classmethod
    def get_format_section(cls):
        return [
            HelpPart(
                f'The date can be specified in ""{cls.metavar}"" format, where DD is '
                f"a number in 1-31 range, and MM is either a number in 1-12 range or "
                f"month short name (first 3 characters). MM-DD format is also accepted. "
                f"Hyphen can be omitted.",
                title="Date format:",
            ),
            HelpPart("Recognised formats list: "),
            HelpPart(cls.format_supported_formats(), indent_shift=1, width_ratio=0.7),
        ]


class MonthYearType(DateTimeType):
    metavar = "MM[-YY]"
    default_help = "Month of interest, see *Date* *format* section."

    @staticmethod
    def get_formats() -> Iterable[str]:
        for v in [*product(["%b", "%m"], ["-", ""], ["%y", "%Y"])]:
            if "-" in v or "%b" in v:
                pass
            else:
                continue
            yield "".join(v)
            yield "".join(reversed(v))
        yield from ("%b", "%m", "%Y")

    @classmethod
    def get_format_section(cls):
        return [
            HelpPart(
                rf"The date can be specified in \"{cls.metavar}\" format, where MM is either "
                "a number in 1-12 range or month short name (first 3 characters), and YY is "
                "either a 2-digit number corresponding to last two digits of a year, or a "
                "4-digit number. If month is specified by a name, the hyphen can be omitted. "
                "Month and year can be swapped.",
                title="Date format:",
            ),
            HelpPart(
                "Note that results of providing a value in ambiguous form are "
                r"unspecified: '02-11' can be interpreted as \"Feb 2011\" as well as \"Nov 2002\"; "
                "in such cases specify a month as a short name ('feb-11') or a year "
                "in a full form ('02-2011')."
            ),
            HelpPart("Recognised formats list: "),
            HelpPart(cls.format_supported_formats(), indent_shift=1, width_ratio=0.9),
        ]


# -----------------------------------------------------------------------------
# Command types


@dataclass(frozen=True)
class CommandAttribute:
    name: str
    char: str
    sorter: int
    description: str
    hidden: bool
    char_big: str  # for "own" format
    fmt: pt.FT
    abbr: str = None

    _values: ClassVar[set[CommandAttribute]] = set()
    _map: ClassVar[dict[str, CommandAttribute]] = dict()

    @classmethod
    def get(cls, name: str) -> CommandAttribute | None:
        return cls._map.get(name, None)

    def __post_init__(self):
        self._values.add(self)
        self._map[self.name] = self

    @abstractmethod
    def get_own_char(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_own_fmt(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_own_label_fmt(self) -> pt.FT:
        raise NotImplementedError

    @abstractmethod
    def get_icon_char_fmt(self) -> pt.FT:
        raise NotImplementedError

    def __eq__(self, other: CommandAttribute) -> bool:
        if not isinstance(other, CommandAttribute):
            return False
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        return hash(f"{self.name}{self.sorter}{self.description}")

    @classmethod
    def values(cls) -> set[CommandAttribute]:
        return cls._values


@dataclass(frozen=True)
class CommandType(CommandAttribute):
    DEFAULT_FMT = FrozenStyle(fg=pt.cv.BLUE)
    DEFAULT_IN_GROUP_FMT = FrozenStyle(DEFAULT_FMT, italic=True)
    DEFAULT_ICON_FMT = FrozenStyle(fg=pt.cv.HI_BLUE)
    HIDDEN_FMT = FrozenStyle(fg=pt.cv.GRAY_35)

    name: str
    char: str
    sorter: int
    description: str = ""
    hidden: bool = False
    char_big: str = None
    fmt: pt.FT = pt.NOOP_STYLE

    def get_own_char(self) -> str:
        return f'{self.char_big or self.char or " ":^3s}'

    def get_own_fmt(self) -> pt.Style:
        base = self.get_icon_char_fmt()
        return FrozenStyle(base, fg=0xFFFFFF, bg=base.fg, dim=True, bold=True)

    def get_own_label_fmt(self) -> pt.FT:
        return self.fmt or self.DEFAULT_FMT

    def get_icon_char_fmt(self, trait: CommandTrait = None) -> pt.Style:
        return pt.merge_styles(
            self.DEFAULT_FMT,
            overwrites=[*filter(None, (trait, self.fmt, FrozenStyle(bold=True)))],
        )

    def get_name_fmt(self, default_in_group: bool) -> pt.Style:
        if self.hidden:
            return self.HIDDEN_FMT
        if default_in_group:
            return self.DEFAULT_IN_GROUP_FMT
        return self.DEFAULT_FMT

    def __hash__(self) -> int:
        return super().__hash__()


@dataclass(frozen=True)
class CommandTrait(CommandAttribute):
    CHAR = "◩"  # "■"

    name: str | None = None
    char: str = CHAR
    sorter: int = 0
    description: str = ""
    hidden: bool = False
    char_big: str = None
    fmt: pt.FT = CommandType.DEFAULT_ICON_FMT

    def get_own_char(self) -> str:
        return self.char

    def get_own_fmt(self) -> pt.FT:
        return self.fmt

    def get_own_label_fmt(self) -> pt.FT:
        return self.fmt

    def get_icon_char_fmt(self) -> pt.FT:
        return pt.Style(self.fmt)

    def __hash__(self) -> int:
        return super().__hash__()


CMDTYPE_INVALID = CommandType(
    name="invalid",
    char="×",
    sorter=0,
    fmt=FrozenStyle(fg=pt.cv.RED),
    description="Something is wrong and this command could not be loaded; therefore, "
    "no help can be shown either. Consider running the same command, but "
    "with '-vv' flag to see the details.",
)
CMDTYPE_GROUP = CommandType(
    name="group",
    char="+",
    sorter=10,
    fmt=FrozenStyle(fg=pt.cv.YELLOW),
    description="This command %s|contains|other commands.",
)
CMDTYPE_BUILTIN = CommandType(
    name="builtin",
    char="·",
    sorter=15,
    char_big="∙",
    description="This is a %s|builtin|es7s/core component written in Python 3 (G2/G3).",
)
CMDTYPE_UNBOUND = CommandType(
    name="unbound",
    char="∘",
    sorter=17,
    char_big="⦿",
    description="This is an %s|unbound|es7s/core component written in Python 3 (G2/G3), "
    "which supports autonomous launching (no extra dependencies, standard Python library only).",
)
CMDTYPE_INTEGRATED = CommandType(
    name="integrated",
    char="~",
    sorter=20,
    description="This is an %s|integrated legacy|component included in es7s/core, "
    "which usually requires es7s/commons shell library (G1/G2).",
)
CMDTYPE_EXTERNAL = CommandType(
    name="external",
    char="^",
    sorter=28,
    description="This is an %s|external standalone|component which is not included in "
    "es7s/core, but is (usually) installed as a part of es7s system. Shell/Golang (G1/G4). "
    "Can be launched directly.",
)
CMDTYPE_DRAFT = CommandType(
    name="draft",
    char="#",
    sorter=30,
    fmt=FrozenStyle(fg=0x888486),
    description="This command is a %s|work in progress|and thus can be unstable or outright broken.",
)

CMDTRAIT_NONE = CommandTrait(
    hidden=True,
)
CMDTRAIT_TEMPLATE = CommandTrait(
    name="template",
    sorter=35,
    fmt=FrozenStyle(fg=pt.cv.GRAY_70),
    description="Source is a %s|static|template.",
)
CMDTRAIT_ADAPTIVE_INPUT = CommandTrait(
    name="adaptin",
    sorter=39,
    fmt=FrozenStyle(fg=pt.cv.MAGENTA),
    description="Support for a standardized input interface.",
    abbr="AI",
)
CMDTRAIT_ADAPTIVE_OUTPUT = CommandTrait(
    name="adaptout",
    sorter=42,
    fmt=FrozenStyle(fg=pt.cv.CYAN),
    description="Output is %s|adjusted|for current terminal size.",
    abbr="AO",
)
CMDTRAIT_X11 = CommandTrait(
    name="x11",
    sorter=50,
    fmt=FrozenStyle(fg=pt.cv.GREEN),
    description="Requires %s|X11|(GUI) environment.",
    abbr="X",
)
CMDTRAIT_G4 = CommandTrait(
    name="g4",
    sorter=60,
    description="Optimized (compiled) implementation.",
    abbr="4",
)
