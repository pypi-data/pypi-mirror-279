# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t  # noqa

from . import *
from .._base import CliBaseCommand
from .._base_opts_params import CMDTYPE_EXTERNAL
from .._foreign import ForeignCommand
from ..autodiscover import AutoDiscover


class _ExternalCommandFactory:
    @staticmethod
    def make_all() -> t.Iterable[CliBaseCommand]:
        if cfgs := AutoDiscover.get_config("cmd-external"):
            for cfg in cfgs.data:
                yield ForeignCommand(cfg.pop("target"), cfg, CMDTYPE_EXTERNAL)


autodiscover_extras = _ExternalCommandFactory.make_all
