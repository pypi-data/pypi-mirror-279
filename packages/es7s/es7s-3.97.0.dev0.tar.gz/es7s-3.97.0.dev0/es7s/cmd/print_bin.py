# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023-2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
# G2 version:
# #!/bin/bash
# #'''''''''''''''''''''''''''''''''''''#
# #             es7s/core               #
# #       (c) 2023 A. Shavykin          #
# #      <0.delameter@gmail.com>        #
# #.....................................#
# [[ $* =~ -?-h(elp)? ]] && echo "Usage :
# $(basename "${0%.*}")" && exit 0; PB(){
# printf "%s\n" "$PATH"| tr : '\n'|sort |
# uniq|xargs -I{} -n1 find {} -maxdepth \
# 1 -executable \( -xtype f -or -type f \
# \) -printf $'%36h\t\e[1m\t%f\x1b[2m\t%l
# ' | sed -Ee '/^\s*\/usr/s/\x1b\[/&34;/1
# /^\s*\/home/s/\x1b\[/&33;/1;s|\S+|&\/|1
# s|( *)'"${HOME//\//\\\/}"'|\1~|;/\S+/!d
# /^\s+/s/\x1b\[/&35;/1;s/(\s)$/\1\x1b[m/
# s/(\t)([^ []+)$/@\x1b[;2m\1\2\x1b[m/' |
# sort -k3,3| tr -s ' '| column -ts$'\t'|
# sed -E 's/(\S+)( *)/\2\1/1'|cat -n;cat\
# <<<____________________>>/dev/null;};PB

from __future__ import annotations

import os
import re
import typing as t
from functools import cached_property
from pathlib import Path

import pytermor as pt

from es7s.shared import sub, SHELL_PATH, build_path, get_logger, FrozenStyle, Styles as BaseStyles
from es7s.shared.enum import RepeatedMode
from ._base import _BaseAction


class action(_BaseAction):
    def __init__(self, mode: RepeatedMode, filter: tuple[str], full_chain: bool, **kwargs):
        self._path_map = PathMap()
        self._mode = mode
        self._full_chain = full_chain
        self._filters = filter
        self._run()

    def _run(self):
        for path in self._get_path():
            if not path:
                continue
            self._path_map.traverse(Path(path))

        for key in sorted(self._path_map.keys()):
            results = self._path_map[key]
            repeat_count = len(results)
            if self._mode == RepeatedMode.ACTIVE:
                self._print_results(key, results[:1], 1)
            elif self._mode == RepeatedMode.GROUPS:
                self._print_results(key, results[:1], repeat_count)
            elif self._mode == RepeatedMode.ALL:
                self._print_results(key, results, repeat_count)
            else:
                raise RuntimeError(f"Invalid dedup mode: {self._mode!r}")

    @classmethod
    def _get_path(cls) -> t.Iterable[str]:
        cp = sub.run_subprocess(
            "echo $PATH",
            shell=True,
            executable=SHELL_PATH,
            env={"PATH": build_path()},
        )
        yield from map(str.strip, cp.stdout.split(":"))

    def _print_results(self, key: str, path_chains: PathChains, repeat_count: int = 0):
        homedir = os.path.expanduser("~")
        for path_chain in path_chains:
            is_active = path_chain == path_chains[0]
            st = ActiveStyles() if is_active else InactiveStyles()
            frags = []

            ep = str(path_chain.entrypoint)
            if is_active:
                ep = ep.removesuffix(key)
            else:
                ep_path, ep_sep, key = ep.rpartition(os.path.sep)
                ep = ep_path+ep_sep
            if ep.startswith(homedir):
                ep = "~" + ep.removeprefix(homedir)
            ep = pt.fit(pt.cut(ep, 24, "^"), 24, ">")
            key = pt.fit(pt.cut(key, 36, "^"), 36, "<")

            if self._filters and all(f not in key for f in self._filters):
                continue

            key_st = st.basename
            if repeat_count > 1:
                if is_active:
                    key_st = pt.Styles.WARNING_LABEL
                    frags += [pt.Fragment(" ⏺", pt.Styles.WARNING_ACCENT)]
                    if self._mode == RepeatedMode.GROUPS:
                        frags += [pt.Fragment(" ◦", st.default)]
                        if repeat_count > 2:
                            frags += [pt.Fragment(f"{repeat_count - 1:<2d}", st.default)]
                        else:
                            frags += [pt.pad(2)]
                    else:
                        frags += [pt.pad(4)]
                else:
                    if self._mode == RepeatedMode.ALL:
                        frags += [pt.Fragment(" ◦" + pt.pad(4), st.default)]
            else:
                frags += [pt.pad(6)]

            if re.match(R"^\s*~/", ep):
                ep_pad, ep_home, ep = ep.partition("~/")
                frags.append(pt.Fragment(ep_pad + ep_home, st.home_prefix))
            elif re.match(R"^\s*/", ep):
                ep_pad, ep_root, ep = ep.partition("/")
                frags.append(pt.Fragment(ep_pad + ep_root, st.root_prefix))
            frags.append(pt.Fragment(ep, st.default))
            frags.append(pt.Fragment("  "+key, key_st))

            squashed = 0
            for symlink in path_chain[1:]:
                is_origin = symlink == path_chain.origin
                if not is_origin and len(path_chain) > 2 and not self._full_chain:
                    squashed += 1
                    continue

                frags.append(pt.Fragment(" → ", st.default))
                if is_origin and squashed > 0:
                    frags.append(pt.Fragment(f"(+{squashed})", st.origin))
                    frags.append(pt.Fragment(" → ", st.default))
                sp = str(symlink)
                if sp.startswith(homedir):
                    sp = "~" + sp.removeprefix(homedir)
                sp_path, sp_sep, sp_base = sp.rpartition(os.path.sep)
                frags.append(pt.Fragment(sp_path + sp_sep, [st.symlink, st.origin][is_origin]))
                frags.append(pt.Fragment(sp_base, [st.symlink, st.basename_origin][is_origin]))
            pt.echo(frags)


class PathChain(list[Path]):
    def __init__(self, path: Path):
        super().__init__()
        self._resolve_chain(path)

    def _resolve_chain(self, path: Path):
        self.append(path)
        if path.is_symlink() and path.exists() and len(self) < 16:
            self._resolve_chain(path.readlink())

    @property
    def entrypoint(self) -> Path:
        return self[0]

    @property
    def origin(self) -> Path:
        return self[-1]


PathChains = list[PathChain]


class PathMap(dict[str, PathChains]):
    def __init__(self):
        super().__init__()
        self._paths_traversed: set[str] = set()

    def traverse(self, path: Path):
        if not os.path.isdir(path) or not os.path.exists(path):
            return

        if (pathstr := str(path)) in self._paths_traversed:
            return
        self._paths_traversed.add(pathstr)

        get_logger().debug(f"Traversing: {path!r}")
        for base, chain in self._read_dir(path):
            if base not in self.keys():
                self[base] = PathChains()
            for pc in self[base]:  # different paths, same origins:
                if pc.origin == chain.origin:
                    return
            self[base].append(chain)

    @classmethod
    def _read_dir(cls, path: Path) -> t.Iterable[tuple[str, PathChain]]:
        for base in os.listdir(path):
            fp = Path(path) / base
            if fp.is_dir():
                continue
            chain = PathChain(fp)
            if os.access(chain.origin, os.X_OK):
                yield base, chain
            continue


class ActiveStyles(BaseStyles):
    @cached_property
    def default(self):
        return pt.NOOP_STYLE

    @cached_property
    def home_prefix(self):
        return FrozenStyle(fg="green", bold=True)

    @cached_property
    def root_prefix(self):
        return FrozenStyle(fg="red", bold=True)

    @cached_property
    def basename(self):
        return FrozenStyle(fg=pt.cv.BLUE, bold=True)

    @cached_property
    def symlink(self):
        return FrozenStyle(fg=pt.cv.GRAY_42, dim=True)

    @cached_property
    def origin(self):
        return FrozenStyle(fg=pt.cv.GRAY_42)

    @cached_property
    def basename_origin(self):
        return FrozenStyle(fg=pt.cv.GRAY_42, bold=True)


class InactiveStyles(BaseStyles):
    @cached_property
    def default(self):
        return FrozenStyle(dim=True)

    @cached_property
    def home_prefix(self):
        return self.default

    @cached_property
    def root_prefix(self):
        return self.default

    @cached_property
    def basename(self):
        return self.default

    @cached_property
    def symlink(self):
        return self.default

    @cached_property
    def origin(self):
        return self.default

    @cached_property
    def basename_origin(self):
        return self.default
