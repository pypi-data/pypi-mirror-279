# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from __future__ import annotations

import psutil

from es7s.cli._base_opts_params import OPT_VALUE_AUTO
from es7s.shared import get_logger


class _MultiThreadedAction:
    def __init__(self, threads: int, auto_threads_limit: int = None, **kwargs):
        super().__init__(**kwargs)

        if threads == OPT_VALUE_AUTO:
            threads = psutil.cpu_count() * 2
            if auto_threads_limit:
                threads = min(threads, auto_threads_limit)

        self._threads = max(1, threads)
        get_logger().info(f"Thread limit is set to: {self._threads}")
