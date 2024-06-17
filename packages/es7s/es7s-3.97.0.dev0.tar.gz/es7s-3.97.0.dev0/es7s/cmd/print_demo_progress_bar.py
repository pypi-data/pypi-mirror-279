# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import math
import pathlib
import typing
from datetime import datetime
from os import stat_result
from stat import filemode
from time import sleep

import pytermor as pt
from es7s_commons import ProgressBar

from es7s.shared import get_stdout, FrozenStyle, get_logger
from ._base import _BaseAction


class action(_BaseAction):
    def __init__(self, pbar: ProgressBar, path: pathlib.Path, slower: int, faster: bool, **kwargs):
        self._path = path
        self._slower = slower
        self._faster = faster
        if self._faster:
            self._slower = 0

        self._run(pbar)

    def _run(self, pbar: ProgressBar):
        pathes = [*filter(lambda f: f.is_dir(), self._path.iterdir())]
        termw = max(0, pt.get_terminal_width())

        idx_pt = 0
        pbar.init_tasks(tasks_amount=len(pathes))
        for pidx, path in enumerate(pathes):
            pbar.next_task(path.absolute().name)
            try:
                children: typing.Sequence[pathlib.Path] = [*path.iterdir()]
            except:
                continue

            pbar.init_steps(len(children))
            for idx, child in enumerate(sorted(children)):
                pbar.next_step(str(child))
                idx_pt += 1
                data = b""
                st: stat_result | None = None
                try:
                    st: stat_result = child.stat()
                    if child.is_file() and not self._faster:
                        with open(child, "rb") as f:
                            data = f.read(12)
                except FileNotFoundError as e:
                    get_logger().warning(e)
                except Exception as e:
                    get_logger().error(e)
                    continue
                if not st:
                    continue

                cc = ""
                for c in data:
                    cc += hex(c).removeprefix("0x").zfill(2) + " "
                while len(cc) < 12 * 3:
                    cc += "·· "
                if self._slower:
                    sleep(math.e**self._slower / 1000)

                fixed_frags = [
                    pt.Fragment(pt.fit(str(idx_pt), 5, ">"), FrozenStyle(dim=True)),
                    pt.Fragment("|", "blue"),
                    pt.FrozenText(pt.format_bytes_human(st.st_size), width=8, align=">"),
                    pt.FrozenText(filemode(st.st_mode), width=12, align=">"),
                    pt.FrozenText(
                        datetime.fromtimestamp(st.st_mtime).strftime("%_e-%b-%Y"),
                        width=12,
                        align=">",
                    ),
                    pt.Fragment("|", "blue"),
                    pt.Fragment(cc),
                ]
                fixed_len = sum(len(ff) for ff in fixed_frags)
                row = pt.Text(
                    *fixed_frags[:2],
                    pt.Text(str(child.resolve()), width=max(0, termw - fixed_len), overflow="…"),
                    *fixed_frags[2:],
                    width=termw,
                )
                get_stdout().echo_rendered(row)
        get_logger().info(" ⏺  " + "Did a lot of hard (fake) work: WIN")
        # stdout.echo(stdout.render()
