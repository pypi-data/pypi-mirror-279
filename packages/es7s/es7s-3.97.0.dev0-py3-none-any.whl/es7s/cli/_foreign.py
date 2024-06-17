# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
from importlib import resources
from typing import TextIO

import pytermor as pt
from es7s_commons import format_attrs

from es7s.shared import (
    LESS_PATH,
    ThemeColor,
    DATA_PACKAGE,
)
from es7s.shared import SHELL_COMMONS_FILE, build_path
from es7s.shared import (
    SubprocessExitCodeError,
    get_logger,
    get_merged_uconfig,
    run_subprocess,
)
from ._base import CliCommand
from ._base_opts_params import CommandType, HelpPart
from ._decorators import catch_and_log_and_exit, cli_command, cli_pass_context
from es7s.shared.path import raise_executable_not_found


class ForeignCliCommand(CliCommand):
    """
    Launch the external/integrated component. PASSARGS are the arguments that
    will be passed to an external app. Long options can also be used, but make
    sure to prepend PASSARGS with "--" to help `click` library to distinguish
    them from its own options. Short options are known to be buggy, better just
    avoid using them on indirect invocations of standalone apps.
    """

    EPILOG_PARTS = [
        HelpPart(
            "This first command will result in 'es7s' command help text, along with "
            "embedded help from the external component, while the second will result in "
            "'watson's direct call and only its own usage being displayed:",
            title="Invocation (generic):",
            group="ex1",
        ),
        HelpPart("  (1) 'es7s exec watson --help'", group="ex1"),
        HelpPart("  (2) 'es7s exec watson -- --help'", group="ex1"),
        HelpPart(
            "Another way to invoke an external component is to call it directly:",
            group="ex2",
        ),
        HelpPart("  (3) 'watson --help'", group="ex2"),
    ]

    def __init__(self, **kwargs):
        kwargs.update(
            {
                "help": self.__doc__,
                "epilog": self.EPILOG_PARTS,
            }
        )
        super().__init__(**kwargs)


class ForeignInvoker:
    def __init__(self, target: str = "bash"):
        self._target = target

    def spawn(self, *args: str, wait=True) -> None:
        cmd_target, cmd_args = self._get_spawn_cmd(*args)
        get_logger().info(f"Launching: {cmd_target} {format_attrs(cmd_args)}")
        code = os.spawnvpe(
            os.P_WAIT if wait else os.P_NOWAIT,
            cmd_target,
            cmd_args,
            self._build_env(),
        )
        if code == 127:
            raise_executable_not_found(self._target)
        if wait and code != 0:
            raise SubprocessExitCodeError(code, args)
        if not wait:
            get_logger().debug(f"Spawned PID: {code}")

    def _get_spawn_cmd(self, *args: str) -> tuple[str, list]:
        return self._target, [self._target, *args]

    def get_help(self) -> str:
        cp = run_subprocess(
            f"{self._target} --help",
            shell=True,
            env=self._build_env(),
            timeout=10,
        )
        if cp.stderr:
            get_logger().non_fatal_exception(cp.stderr)
        return cp.stdout

    def _build_env(self) -> dict:
        logger = get_logger()
        commons_path = resources.path(DATA_PACKAGE, SHELL_COMMONS_FILE)
        user_repos_path = (
            get_merged_uconfig().get_section("general").get("user-repos-path", fallback="")
        )
        theme_seq = ThemeColor().to_sgr()
        result = {
            # ---[@temp]--- filter out all G1/G2 es7s env vars:
            **{k: v for (k, v) in os.environ.items() if not k.lower().startswith("es7s")},
            # ---[@temp]---
            "PATH": build_path(),
            # "COLORTERM": os.environ.get("COLORTERM"),
            # "TERM": os.environ.get("TERM"),
            "ES7S_SHELL_COMMONS": commons_path,
            "ES7S_DATA_DIR": resources.path(DATA_PACKAGE, "."),
            "ES7S_USER_REPOS_PATH": user_repos_path,
            "ES7S_THEME_COLOR_SGR": ";".join(map(str, theme_seq.params)),
        }
        for k, v in sorted(result.items(), key=lambda k: k):
            logger.debug(
                f"Subprocess environ: {k:30s}={format_attrs(v)}"
            )  # , out_plain=False, out_sanitized=True)
        return result


def ForeignCommand(target: str, attributes: dict, type: CommandType) -> ForeignCliCommand:
    inv_ = ForeignInvoker(target)
    cmd = lambda ctx, inv=inv_: inv.spawn(*ctx.args)
    cmd = catch_and_log_and_exit(cmd)
    cmd = cli_pass_context(cmd)
    cmd = cli_command(
        **(attributes or dict()),
        name=target.removesuffix(".sh"),
        cls=ForeignCliCommand,
        type=type,
        ignore_unknown_options=True,
        allow_extra_args=True,
        ext_help_invoker=lambda ctx, inv=inv_: inv.get_help(),
        usage_section_name="Usage (generic)",
        include_common_options_epilog=False,
    )(cmd)
    return cmd


class Pager(ForeignInvoker):
    def __init__(self, max_line_len: int = None):
        target = LESS_PATH
        if os.getenv("NOPAGER"):
            target = "cat"
        elif pager := os.getenv("PAGER"):
            target = pager
        super().__init__(target=target)

        term_width = pt.get_terminal_width(pad=0)
        self._scrollx = term_width // 2

        if max_line_len and max_line_len < term_width * 1.5:
            self._scrollx = term_width // 5

    def open(self, file: TextIO, close_after=True) -> None:
        args = []
        if self.is_default_target:
            args = [f"-# {self._scrollx}", "-RF"]
        args += [file.name]

        try:
            super().spawn(*args, wait=True)
        finally:
            if close_after and not file.closed:
                file.close()

    @property
    def is_default_target(self) -> bool:
        return self._target == LESS_PATH

    def _build_env(self) -> dict:
        env = super()._build_env()
        env.pop("LESSOPEN", None)
        return env
