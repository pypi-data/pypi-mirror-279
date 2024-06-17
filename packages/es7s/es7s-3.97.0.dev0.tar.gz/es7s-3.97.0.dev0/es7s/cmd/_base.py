# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations
import abc
from abc import abstractmethod
from typing import overload

from es7s.shared import (
    UserConfigSection,
    uconfig,
)


class _BaseAction(metaclass=abc.ABCMeta):
    def __init__(self, **kwargs):
        ...

    @abstractmethod
    def _run(self, *args, **kwargs):  # @TODO are *args necessary here?
        ...

    @staticmethod
    @overload
    def uconfig(origin) -> UserConfigSection:
        ...

    @classmethod
    @overload
    def uconfig(cls) -> UserConfigSection:
        ...

    def uconfig(self) -> UserConfigSection:
        return uconfig.get_for(self)
