# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from functools import partial

_isfilled = lambda v: bool(v) and len(str(v).strip())

filtere = partial(filter, _isfilled)
"""Shortcut for filtering out falsy AND empty values from sequences."""


def filterev(mapping: dict) -> dict:
    """Shortcut for filtering out falsy AND empty values from mappings."""
    return dict(filter(lambda kv: _isfilled(kv[1]), mapping.items()))
