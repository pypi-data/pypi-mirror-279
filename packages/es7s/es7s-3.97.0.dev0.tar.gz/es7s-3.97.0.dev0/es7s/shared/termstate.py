# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from logging import getLogger

import pytermor as pt
from es7s_commons import TerminalState

from .io_ import IoProxy, get_stdout
from .uconfig import get_merged


class ProxiedTerminalState(TerminalState):
    def __init__(self, io_proxy: IoProxy = None):
        super().__init__(io_proxy or get_stdout())
        self._debug = get_merged().termstate_debug_mode
        self._force_esq = self._io.color

    def assign_proxy(self, io_proxy: IoProxy):
        self._io = io_proxy
        getLogger(__package__).debug(f"TSC: Switched to {self._io}")

    def _echo(self, sequence: pt.ISequence):
        self._io.echo(sequence, bypass=True)  # do not allow to intercept and buffer these
