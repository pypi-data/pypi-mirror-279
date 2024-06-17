# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
import re
import stat
import typing as t
from importlib import resources

import click
from es7s_commons import format_attrs

from es7s.shared import (
    USER_ES7S_BIN_DIR,
    get_logger,
    run_subprocess,
    DATA_PACKAGE,
)
from es7s.shared import WMCTRL_PATH
from es7s.shared.enum import FilterType, SelectorType
from ._base import _BaseAction


class action(_BaseAction):
    def __init__(
        self,
        ctx: click.Context,
        indexes: t.Sequence[int],
        filter: FilterType,
        selector: SelectorType,
        shell: bool,
        dry_run: bool,
        **kwargs,
    ):
        self._config_section = f"exec.{ctx.command.name}"

        if not (filter_idxs := set(indexes)):
            filter_idxs = self.uconfig().get("indexes", set, int)

        if shell:
            self._update_shell_script(filter_idxs, filter, selector, dry_run)
        else:
            self._run(filter_idxs, filter, selector, dry_run)

    def _update_shell_script(
        self,
        filter_idxs: set[int],
        filter_type: FilterType,
        selector_type: SelectorType,
        dry_run: bool,
    ):
        logger = get_logger()

        filter_regex = "^$"
        if len(filter_idxs) > 0:
            filter_regex = "|".join(map(str, filter_idxs))

        tpl = resources.read_text(DATA_PACKAGE, "switch-wspace-turbo.tpl")
        tpl_params = {
            "filter_name": filter_type.value,
            "filter_regex": filter_regex,
            "selector_name": selector_type.value,
            "wmctrl_path": WMCTRL_PATH,
        }
        logger.debug(f"Substitution values: {format_attrs(tpl_params)}")

        script = tpl % tpl_params
        logger.debug(f"Template length: {len(tpl)}")
        logger.debug(f"Script length: {len(script)}")

        script_path = USER_ES7S_BIN_DIR / "switch-wspace-turbo"
        msg = f"Writing the result script: {script_path}"
        if dry_run:
            logger.info(f"[DRY-RUN] {msg}")
            return  # @TODO notice instead, the difference is that it's going to stderr even at -v 0
        logger.info(msg)

        with open(script_path, "wt") as f:
            f.write(script)

        st = os.stat(script_path)
        logger.debug('Setting the "+executable" flag')
        os.chmod(script_path, st.st_mode | stat.S_IEXEC)

    def _run(
        self,
        filter_idxs: set[int],
        filter_type: FilterType,
        selector_type: SelectorType,
        dry_run: bool,
    ):
        logger = get_logger()

        allowed_idxs = []
        active_idx = None

        for wspace_str in self._get_wspace_list():
            if (m := re.search(r"^(\d+)\s*([*-]).+$", wspace_str)) is None:
                continue

            idx = int(m.group(1))
            if m.group(2) == "*":
                active_idx = idx
                logger.debug(f"Workspace {idx}: DENIED (current active)")
                continue

            if not self._is_allowed_by_filter(idx, filter_idxs, filter_type):
                continue

            logger.debug(f"Workspace {idx}: ALLOWED")
            allowed_idxs.append(idx)

        logger.debug(
            f"Allowed target workspaces ({len(allowed_idxs)}): " + format_attrs(allowed_idxs)
        )
        if active_idx is None:
            logger.warning("Failed to determine active workspace")

        if len(allowed_idxs) == 0:
            logger.info("No allowed target workspaces found")
            return

        target_idx = self._select(allowed_idxs, active_idx, selector_type)
        logger.debug(f"Target workspace: {target_idx}")

        if dry_run:
            logger.info(f"[DRY-RUN] Switching workspace to {target_idx}")
            return
        self._switch_to_wspace(target_idx)

    def _get_wspace_list(self) -> list[str]:
        return run_subprocess(WMCTRL_PATH, "-d").stdout.splitlines()

    def _is_allowed_by_filter(
        self, idx: int, filter_idxs: set[int], filter_type: FilterType
    ) -> bool:
        if filter_type == FilterType.OFF:
            return True

        if filter_type == FilterType.BLACKLIST:
            return idx not in filter_idxs

        if filter_type == FilterType.WHITELIST:
            return idx in filter_idxs

        raise RuntimeError(f"Invalid filter: {filter_type}")

    def _select(self, allowed_idxs: list[int], active_idx: int, selector_type: SelectorType) -> int:
        if selector_type == SelectorType.FIRST:
            return allowed_idxs[0]
        if selector_type == SelectorType.CYCLE:
            allowed_next_to_active_idxs = [*filter(lambda idx: idx > active_idx, allowed_idxs)]
            if len(allowed_next_to_active_idxs) == 0:
                return allowed_idxs[0]
            return allowed_next_to_active_idxs[0]
        raise RuntimeError(f"Invalid selector: {selector_type}")

    def _switch_to_wspace(self, target_idx):
        run_subprocess(WMCTRL_PATH, f"-s{target_idx}")
