# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import pytermor as pt

from es7s.cli._base import NWMarkup
from es7s.shared import inspect
from ._base import _BaseAction


class action(_BaseAction):
    def __init__(self, *args, **kwargs):
        self._run()

    def _run(self):
        nwml = NWMarkup()
        inspect(nwml._filters)
        inspect(pt.DualFormatterRegistry)
        inspect(pt.DualFormatter())
        inspect(pt.TemplateEngine())
        inspect(pt.SeqIndex)
        a = 1
        b = [a, 2, 3, 4]
        c = [b, 5, 6, 7, 8]
        d = [c, 9, 10]
        b.append(d)
        inspect(d)
