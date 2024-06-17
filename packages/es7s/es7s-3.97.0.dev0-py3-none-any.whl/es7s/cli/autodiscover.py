# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import os
import re
import sys
import typing as t
from functools import lru_cache
from importlib.abc import Traversable
from pathlib import Path
from typing import Iterable

import pytermor as pt

from es7s.shared import get_logger, get_app_config_yaml, get_stdout, Styles, is_command_file
from ._base import CliGroup, CliCommand, Context, HelpFormatter, InvokerT
from ._base_opts_params import (
    CMDTYPE_INTEGRATED,
    CMDTRAIT_TEMPLATE,
    CommandType,
    CMDTYPE_INVALID,
)
from ._decorators import catch_and_log_and_exit, cli_command, cli_pass_context
from es7s.shared.exception import AutodiscoverValidationError

AutoDiscoverExtras = t.Callable[[], Iterable["CliBaseCommand"]]

AutoConfigData = dict[str, dict[str]] | list[dict[str]]


class AutoConfig:
    """
    definitions from yaml configs, can be:
      * dict {<module_name>: {<attrs>}, ...} for regular es7s modules,
      * list [{<attrs>}, ...]                for external configs
    """

    def __init__(self, cfg_path: str, data: AutoConfigData = None):
        self._cfg_path = cfg_path
        self._data: AutoConfigData = data or {}

    @property
    def data(self) -> AutoConfigData:
        return self._data

    def get(self, key: str) -> any:
        return self.data.get(key)

    def validate(self):
        if isinstance(self._data, list):  # external config (without corresponding es7s modules)
            return

        from importlib.util import find_spec

        try:
            error_msgs = []
            for modname in self._data.keys():
                try:
                    if not find_spec(modname):
                        error_msgs.append(f"Module not found: {modname!r}")
                except ModuleNotFoundError as e:
                    error_msgs.append(str(e))
            if error_msgs:
                raise AutodiscoverValidationError(self._cfg_path, *error_msgs)

        except AutodiscoverValidationError as e:  # DOES NOT interrupt module loading
            get_logger(require=False).warning(str(e))


class AutoDiscover:
    INLINED_HELP_REGEX = re.compile(R"#\[?\s*es7s/core\s*\|([^]]+)]?")

    @staticmethod
    @lru_cache
    def get_config(name: str, validate=True) -> AutoConfig | None:
        try:
            cfg = AutoConfig(*get_app_config_yaml(name))
        except FileNotFoundError as e:  # INTERRUPTS module loading
            get_logger(require=False).error(str(e))
            return None

        if validate:
            cfg.validate()
        return cfg

    @classmethod
    def run(cls: AutoDiscover, command, filepath, extras: AutoDiscoverExtras = None):
        import importlib.resources

        subpkg = os.path.relpath(os.path.dirname(filepath), os.path.dirname(__file__))
        pkg = (__package__ + "." + subpkg.replace("/", ".")).rstrip(".")

        for el in importlib.resources.files(pkg).iterdir():
            if el.name.startswith("_"):
                continue
            try:
                if cmd := cls._element_to_command(el, pkg):
                    if defsub := getattr(command, "default_subcommand", None):
                        if cmd.name == defsub:
                            cmd.set_default_in_group()
                    command.add_command(cmd)
            except Exception as e:
                target = f"{subpkg}/{el.name}" + ("/" if el.is_dir() else "")
                get_logger(require=False).warning('Autodiscover skipping "%s": %s' % (target, e))

                # @todo figure out how to handle these cases when logger is not initialized yet
                if re.search(R"-v+|--verbose", " ".join(map(str, sys.argv))):
                    get_logger(require=False).exception(e)

                command.add_command(InvalidCommandPlaceholder(el.name, CMDTYPE_INVALID, e))

        if extras:
            command.add_commands(extras())

        if isinstance(command, CliGroup) and not len(command.get_commands()):
            get_logger(require=False).warning(f"Empty command group: {pt.get_qname(command)}")

    @classmethod
    def _element_to_command(cls: AutoDiscover, el: Traversable | Path, pkg: str) -> t.Any:
        name, ext = os.path.splitext(el.name)
        cfgkey = f"{pkg}.{name}"

        if el.is_dir() or (el.is_file() and el.name.startswith("_group")):
            if cfgs := AutoDiscover.get_config("cmd-autogroup"):
                return cls._register_group(el, pkg, cfgs.get(cfgkey))
            raise RuntimeError(f"Autogroup config not found")

        if el.is_file() and ext:
            if not is_command_file(name, ext):  # skipping temporary files
                return None
            match ext:
                case ".py":
                    return cls._register_builtin(f".{name}", pkg)
                case ".txt" | ".ptpl" | ".dot":
                    if cfgs := AutoDiscover.get_config("cmd-template", validate=False):
                        return cls._register_template(el, pkg, cfgs.get(cfgkey))
                case ".sh":
                    if cfgs := AutoDiscover.get_config("cmd-integrated"):
                        return cls._register_integrated(el, pkg, cfgs.get(cfgkey))
                case _:
                    raise RuntimeError(f"Unknown extension: {el}")
            raise RuntimeError(f"Command config not found for {str(el)!r}")
        raise RuntimeError(f"Unknown element at {str(el)!r}")

    @classmethod
    def _register_group(cls, el: Traversable | Path, pkg: str, cfg: dict) -> t.Any:
        if not cfg:
            raise RuntimeError(f"No group config")
        import importlib

        name = el.name.removesuffix(".py")
        mod = importlib.import_module("." + name, pkg)

        if fn := getattr(mod, "group", None):
            return fn

        from ._decorators import cli_group

        extras = getattr(mod, "autodiscover_extras", None)
        filepath = os.path.abspath(str(el.joinpath("__init__.py")))
        grp = cli_group(name=filepath, autodiscover_extras=extras, **cfg)(lambda: None)
        return grp

    @classmethod
    def _register_builtin(cls, modname: str, pkg: str) -> InvokerT | None:
        import importlib

        mod = importlib.import_module(modname, pkg)
        return getattr(mod, "invoker", None)

    @classmethod
    def _register_template(cls, el: Traversable | Path, pkg: str, cfg: dict) -> t.Any:
        from ._template import TemplateCommand

        filepath = os.path.abspath(str(el))
        kw_ = {}
        if cfg:
            kw_ = pt.filternv(
                dict(
                    sectgap=cfg.pop("sectgap", None),
                    sectsize=cfg.pop("sectsize", None),
                    gap=cfg.pop("gap", None),
                    rows_first=cfg.pop("rows_first", None),
                )
            )
        else:
            cfg = {}
        if "help" not in cfg.keys():
            if inlined := cls._extract_inlined_help(el):
                cfg["help"] = inlined

        scmd = lambda fp=filepath, kw=kw_: TemplateCommand(fp).run(**kw)
        scmd = catch_and_log_and_exit(scmd)
        scmd = cli_command(
            name=el.name,
            traits=[CMDTRAIT_TEMPLATE],
            **(cfg or dict(help=f"/*substitute {os.path.basename(el)}*/")),
        )(scmd)
        return scmd

    @classmethod
    def _register_integrated(cls, el: Traversable | Path, pkg: str, cfg: dict) -> t.Any:
        from ._foreign import ForeignCommand

        if not cfg:
            cfg = dict()
        if not cfg.get("short_help"):
            if inlined := cls._extract_inlined_help(el):
                cfg["short_help"] = inlined
        if not cfg.get("short_help"):
            cfg["short_help"] = f"/*run {os.path.basename(el)}*/"
        fcmd = ForeignCommand(os.path.abspath(str(el)), cfg, CMDTYPE_INTEGRATED)
        return fcmd

    @classmethod
    def _extract_inlined_help(cls, el: Traversable | Path) -> str:
        with el.open("rt", buffering=True) as f:
            for line in f.readlines(1024):
                if m := cls.INLINED_HELP_REGEX.search(line):
                    return m.group(1)


class InvalidCommandCliPlaceholder(CliCommand):
    def __init__(self, **kwargs):
        self._err: Exception = kwargs.pop("err")
        super().__init__(**kwargs)

    def run(self):
        get_logger().exception(self._err)
        raise RuntimeError(f"Command load failed") from self._err

    def format_help(self, ctx: Context, formatter: HelpFormatter):
        super().format_help(ctx, formatter)
        formatter.write_paragraph()
        with formatter.indentation():
            formatter.write_text(get_stdout().render(self._format_error(), Styles.ERROR_ACCENT))
        get_stdout().echo(formatter.getvalue())
        formatter.buffer.clear()

    def _format_error(self) -> str:
        err_cls = pt.get_qname(self._err)
        return f"{err_cls}: {self._err}"

    def _make_short_help(self, **kwargs) -> str:
        return f"++Load++ ++failed:++ /*{self._err}*/"


def InvalidCommandPlaceholder(name: str, cmdtype: CommandType, err: Exception):
    cmd = lambda ctx: t.cast(InvalidCommandCliPlaceholder, ctx.command).run()
    cmd = catch_and_log_and_exit(cmd)
    cmd = cli_pass_context(cmd)
    cmd = cli_command(
        name=name,
        cls=InvalidCommandCliPlaceholder,
        type=cmdtype,
        ignore_unknown_options=True,
        allow_extra_args=True,
        include_common_options_epilog=False,
        err=err,
    )(cmd)
    return cmd
