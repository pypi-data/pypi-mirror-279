# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os.path
import re
import tempfile
from importlib import resources
from os.path import expanduser
from pathlib import Path

from .exception import ExecutableNotFoundError
from .. import APP_NAME

# @TODO let the shell to find a binary in PATH or find it ourselves
SHELL_PATH = "/bin/bash"
LESS_PATH = "/usr/local/bin/less"
ENV_PATH = "/bin/env"
GIT_PATH = "/usr/bin/git"
WMCTRL_PATH = "/bin/wmctrl"
DOCKER_PATH = "/bin/docker"
TMUX_PATH = "/usr/local/bin/tmux"
GH_LINGUIST_PATH = "/usr/local/bin/github-linguist"
XDOTOOL_PATH = "/usr/bin/xdotool"
DCONF_PATH = "/usr/bin/dconf"
GIMP_CONFIG_PATH = Path(os.path.expanduser("~/.config/GIMP/2.10/"))
TERMINAL_EXECUTABLE = "gnome-terminal"

DATA_PACKAGE = f"{APP_NAME}.data"
DIST_PACKAGE = f"{APP_NAME}.distx"
GIT_LSTAT_DIR = "lstat-cache"

USER_ES7S_BIN_DIR = Path(os.path.expanduser("~/.es7s/bin"))
USER_ES7S_DATA_DIR = Path(os.path.expanduser("~/.es7s/data"))
USER_XBINDKEYS_RC_FILE = Path(os.path.expanduser("~/.xbindkeysrc"))

SHELL_COMMONS_FILE = "es7s-shell-commons.sh"

ESQDB_DATA_PIPE = os.path.join(tempfile.gettempdir(), "es7s-esqdb-pipe")


def get_user_config_dir() -> str:
    import click

    return click.get_app_dir(APP_NAME)


def get_user_data_dir() -> Path:
    return USER_ES7S_DATA_DIR


def get_app_config_yaml(name: str) -> tuple[str, dict | list]:
    import yaml

    filename = f"{name}.yml"
    user_path = os.path.join(USER_ES7S_DATA_DIR, filename)

    if os.path.isfile(user_path):
        with open(user_path, "rt") as f:
            return user_path, yaml.safe_load(f.read())
    else:
        f = resources.open_text(DATA_PACKAGE, filename)
        try:
            return f.name, yaml.safe_load(f)
        finally:
            f.close()


SMALLEST_PIXEL_7 = "Smallest_Pixel_7_Regular.ttf"


def get_font_file(name: str) -> Path | None:
    path_in_data = get_user_data_dir() / "fonts" / name
    if path_in_data.exists():
        return path_in_data
    return None


def is_command_file(name: str, ext: str, is_internal=False):
    """
    Return True if file contains es7s CLI command and False otherwise.
    Implied that provided file is located in es7s.cli package dir.

    :param is_internal: if True, executables starting with '_' or '.' are
                        considered command files, and vice versa.
    """
    if re.match(r"[_.]", name):
        if not is_internal:
            return False
    if re.match(r"\.(.*_|pyc)$", ext):
        return False
    return True


def build_path() -> str:
    current = os.environ.get("PATH", "").split(":")
    filtered = ":".join(
        [
            str(USER_ES7S_BIN_DIR),  # add top-priority G3 path
            # ---[@temp]----- remove all deprecated es7s parts from PATH:
            # *filter(lambda s: "es7s" not in s, current),
            *current,
            expanduser("~/bin/es7s"),
            # ---[@temp]----- ^ restore legacy path
        ]
    )
    return filtered


def find_executable(name: str) -> str:
    from .sub import run_subprocess

    cp = run_subprocess("which", name, check=False)
    return cp.stdout.strip()


def find_system_executable(name: str) -> str:
    from .sub import run_subprocess

    # default paths only
    cp = run_subprocess("which", name, env={"PATH": "/usr/local/bin:/usr/bin"})
    return cp.stdout.strip()


def raise_executable_not_found(target_path: str):
    def __diagnose(p: str):
        if not os.path.exists(p):
            return f"Not found: {p!r}"
        if not os.path.isfile(p):
            return f"Not a file: {p!r}"
        if not os.access(p, os.R_OK):
            return f"Not readable: {p!r}"
        if not os.access(p, os.X_OK):
            return f"Not executable: {p!r}"
        with open(p, "rt") as f:
            try:
                line1 = f.readline()
                if not line1.startswith("#!"):
                    return f"Missing shebang directive: {p!r}"
                intp_path = line1.removeprefix("#!").strip()
                if intp_result := __diagnose(intp_path):
                    return f"Interpreter problem: {intp_result}: {intp_path!r}"
                return None  # seems fine, subprocess issue maybe

            except UnicodeDecodeError:
                return None  # looks like a binary

    raise ExecutableNotFoundError(target_path, __diagnose(target_path))


def is_x11() -> bool:
    display = os.environ.get("DISPLAY", None)
    return display and not display.isspace()
