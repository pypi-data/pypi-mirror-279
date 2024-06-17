# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import builtins
import typing as t
from dataclasses import dataclass

import pytermor as pt
from pytermor import FT, RT, get_terminal_width, IRenderer, Composite

Size = int | float | None


AUTO: Size = None


@dataclass(frozen=True)
class ElasticSetup:
    min_width: Size = AUTO
    max_width: Size = AUTO
    align: pt.Align | str = pt.Align.LEFT
    overflow: bool = None

    @classmethod
    def size_to_chars(cls, size: Size, container_width: int) -> int:
        if size is None:
            return container_width
        if isinstance(size, int):
            return size
        if isinstance(size, float):
            return round(size * container_width)
        raise TypeError(f"Size should be int/float/None, got: {type(size)}")


class ElasticFragment(pt.Fragment, t.Sized):
    def __init__(
        self,
        string: str = "",
        fmt: FT = None,
        *,
        close_this: bool = True,
        close_prev: bool = False,
        es: ElasticSetup = ElasticSetup(),
    ):
        self._elastic_setup = es
        super().__init__(string, fmt, close_this=close_this, close_prev=close_prev)

    @property
    def elastic_setup(self) -> ElasticSetup:
        return self._elastic_setup

    def get_min_width(self, container_width: int) -> int:
        if self._elastic_setup.min_width:
            return ElasticSetup.size_to_chars(self._elastic_setup.min_width, container_width)
        return len(self)

    def get_max_width(self, container_width: int) -> int:
        if self._elastic_setup.max_width:
            return ElasticSetup.size_to_chars(self._elastic_setup.max_width, container_width)
        return len(self)


class ElasticContainer(pt.Composite):
    def __init__(self, *parts: RT, width: Size = AUTO, gap: Size = 2):
        super().__init__(*parts)
        self._width: Size = width
        self._gap: Size = gap

    def __add__(self, other: RT) -> Composite:
        return super().__add__(other)

    def render(self, renderer: IRenderer | t.Type[IRenderer] = None) -> str:
        avail_width = ElasticSetup.size_to_chars(self._width, get_terminal_width())
        if avail_width < 1:
            return ""

        min_widths = []
        max_widths = []
        for part in self._parts:
            if isinstance(part, ElasticContainer):
                raise NotImplementedError

            if isinstance(part, ElasticFragment):
                min_widths.append(part.get_min_width(avail_width))
                max_widths.append(part.get_max_width(avail_width))
            else:
                content_width = len(part)
                min_widths.append(content_width)
                max_widths.append(content_width)

        gap_width = ElasticSetup.size_to_chars(self._gap, avail_width)
        gaps_width = gap_width * (len(self._parts) - 1)
        min_width = sum(min_widths) + gaps_width
        max_width = sum(max_widths) + gaps_width

        if min_width < avail_width < max_width:
            result_widths = min_widths.copy()
            free_width = avail_width - min_width
            idx = 0
            while free_width:
                if result_widths[idx] < max_widths[idx]:
                    free_width -= 1
                    result_widths[idx] += 1
                idx += 1
                if idx >= len(self._parts):
                    idx = 0
        elif avail_width <= min_width:
            result_widths = min_widths
        else:
            result_widths = max_widths

        result = ""
        for (idx, part) in enumerate(self._parts):
            if idx > 0:
                result += pt.pad(gap_width)

            result_width = result_widths.pop(0)
            use_overflow = len(part) > result_width

            if isinstance(part, ElasticFragment):
                align = part.elastic_setup.align
                if part.elastic_setup.overflow is not None:
                    use_overflow = part.elastic_setup.overflow
            elif isinstance(part, pt.FrozenText):
                align = part._align
            else:
                align = pt.Align.LEFT
            tx = pt.Text(
                *part.as_fragments(),
                width=result_width,
                align=align,
                overflow=["", pt.OVERFLOW_CHAR][use_overflow],
            )
            result += tx.render(renderer)

        return result

    def __len__(self) -> int:
        raise NotImplementedError

    @property
    def has_width(self) -> bool:
        return True


def guess_width(s: str) -> int:
    return sum(pt.guess_char_width(c) for c in s)


# -------------------------------------------------


class Sentinel:
    def __str__(self):
        return __package__ + self.__class__.__name__

    def __bool__(self):
        return False


# -------------------------------------------------

_KT = t.TypeVar("_KT")
_VT = t.TypeVar("_VT")
_CT = t.TypeVar("_CT")


def getn(data: t.Mapping[_KT, _VT], key: _KT, cls: t.Type[_CT] = None) -> _CT | None:
    """
    "Nullable" wrapper around `get()`, which not only allows `key` to be missing, but
    also catches type checking/conversion errors and returns *None* in both
    cases.
    """
    try:
        return get(data, key, cls, required=False)
    except ValueError:
        return None


def getr(data: t.Mapping[_KT, _VT], key: _KT, cls: t.Type[_CT] = None) -> _CT:
    """
    "Required" wrapper around `get()`, which always requires `key` to be present.

    :raises KeyError:   if key is not found.
    """
    return get(data, key, cls, required=True)


def get(data: t.Mapping[_KT, _VT], key: _KT, cls: t.Type[_CT] = None, required=True) -> _CT | None:
    """
    Get nested dictionary value; key can be specified as "aa.bb.ccc" -- a composite
    of three keys of each of nested *dict*\\ s.

    :param data:  input mapping instance.
    :param key:   can be any type, but if it is *str*, then special handling of composite
                  keys is invoked.
    :param cls:   if not *None*, the result value will be of specified type or ValueError
                  is raised; if *None*, no type conversion/checking is performed.
    :param required:    if specified key does not exist, raise KeyError when `required` is
                        *True*, and return *None* otherwise.
    :raises KeyError:   if key is not found and `required` is *True*.
    :raises ValueError: if `cls` is not *None* and type conversion failed.
    :returns:     value from `data` of `cls` type found at specified `key`, or *None*.
    """
    if isinstance(key, str):
        while "." in key:
            cur_key, _, key = key.partition(".")
            data = get(data, cur_key, dict, required)

    val = data.get(key, _MISSING)
    if val is _MISSING:
        if required:
            raise KeyError(f"Data is missing {key!r} field")
        return None
    if cls is None:
        return val

    try:
        if hasattr(builtins, cls.__name__):
            return cls(val)
        if not issubclass(type(val), cls):
            raise TypeError(f"{val!r} is not a subclass of {cls!r}")
    except ValueError as e:
        raise ValueError(f"Failed to represent {val!r} as {cls!r}") from e

    return val


_MISSING = Sentinel()


# ---------------------------------------------------

_COLORBOX_CHAR_BY_ALPHA = " " + ((64 * "░") + (64 * "▒") + (64 * "▓") + (64 * "█"))[1:]


def format_colorbox(val: int, a256: int = None) -> pt.Text:
    smpst = pt.Style(fg=val)
    fgst = pt.Style(bg=val).flip().autopick_fg()
    if fgst.fg.hsv.value < 0.3:
        fgst.fg = pt.NOOP_COLOR

    text = pt.Text()
    if a256 is None:
        ch = _COLORBOX_CHAR_BY_ALPHA[-1]
    else:
        ch = _COLORBOX_CHAR_BY_ALPHA[a256 % 256]
        text += f" {a256/2.55:>3.0f}% "
    text += (ch * 2, smpst)

    text += (f" {val:06x} ", fgst), pt.Fragment("│", pt.cv.GRAY_23)
    return text


def condecorator(dec, condition):
    def decorator(func):
        if not condition:
            return func
        return dec(func)

    return decorator
