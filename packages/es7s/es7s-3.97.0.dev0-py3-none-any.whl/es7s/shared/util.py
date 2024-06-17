# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t
from collections.abc import Iterable

_KT = t.TypeVar("_KT")
_VT = t.TypeVar("_VT")


def multisplit(
    items: Iterable[_VT],
    cond: t.Callable[[_VT], _KT],
    keys: t.List[_KT] = None,
) -> dict[_KT, list[_VT]]:
    d = {k: [] for k in (keys or [])}
    for item in items:
        result = cond(item)
        try:
            if result not in d.keys():
                d[result] = []
            d[result].append(item)
        except TypeError as e:
            raise ValueError("Condition result should be hashable") from e
    return d


def boolsplit(items: Iterable[_VT], cond: t.Callable[[_VT], bool]) -> tuple[list[_VT], list[_VT]]:
    d = multisplit(items, cond, [True, False])
    return d[True], d[False]
