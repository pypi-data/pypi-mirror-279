# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import importlib.resources
from importlib.abc import Traversable
from pathlib import Path

from .path import DATA_PACKAGE


def get_res_dir(subpath: str | Path = None) -> Path | Traversable:
    result = importlib.resources.files(DATA_PACKAGE)
    if subpath:
        return result.joinpath(subpath)
    return result


def get_demo_res(subpath: str | Path = None) -> Path | Traversable:
    return get_res_dir(Path("demo", subpath))
