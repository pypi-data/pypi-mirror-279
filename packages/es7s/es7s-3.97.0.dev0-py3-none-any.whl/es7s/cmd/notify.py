# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os

from es7s.shared import run_subprocess
from es7s.shared.enum import EventStyle
from ._base import _BaseAction


class action(_BaseAction):
    def __init__(self, *args, **kwargs):
        self._run(*args, **kwargs)

    def _run(self, ident: str, message: str, style: EventStyle, **kwargs):
        match ident:
            case "pytermor":
                icon = "/home/a.shavykin/dl/pytermor/docs/_static_src/logo-white-bg.svg"
            case "es7s/core":
                icon = os.path.join(os.path.dirname(__file__), "..", "..", "..", "logo.svg")
            case _:
                icon = style.filename

        run_subprocess(  # @temp
            "notify-send",
            "-i",
            icon,
            ident,
            message,
            check=True,
        )
