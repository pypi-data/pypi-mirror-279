# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

from .._decorators import (
    catch_and_log_and_exit,
    cli_argument,
    cli_command,
    cli_flag,
)


@cli_command(__file__, "list directory contents with bells and whistes")
@cli_argument("file", type=str, required=False, nargs=-1)
@cli_flag("-g", "--groups", help="Display group column.")
@cli_flag("-G", "--grid", help="Display names and icons as a grid, rows first.")
@cli_flag("-h", "--hard-links", help="Display amount of hard links to the file.")
@cli_flag("-i", "--inode", help="Display index number of each file.")
@cli_flag(
    "-L",
    "--dereference",
    help="Follow the symlinks and print actual file properties instead of link file properties.",
)
@cli_flag("-n", "--numeric", help="Show user/group numeric IDs instead of resolved names.")
@cli_flag("-o", "--octal-perms", help="Display extra column with permissions in octal form.")
@cli_flag("-q", "--quote-names", help="Enclose names in quotes, escape non-printables.")
@cli_flag("-r", "--reverse", help="Reverse sorting order.")
@cli_flag("-R", "--recursive", help="Descend into subdirectories.")
@cli_flag("-s", "--sort-by-size", help="Sort entries by file size, biggest last.")
@cli_flag("-t", "--sort-by-time", help="Sort entries by modification time, newest last.")
@cli_flag("-x", "--sort-by-ext", help="Sort entries alphabetically by extension.")
@cli_flag("-X", "--rows-first", help="(with '-G' only) Fill table horizontally rather than vertically.")
@cli_flag(
    "--fallback-icons",
    help="Use shorter icon set (5 items) which should be supported by literally everything down "
    "to a potato (inclusive). Useful when a terminal's font does not support Nerd Fonts "
    "file type icons (glyphs around U+E650).",
)
@catch_and_log_and_exit
def invoker(*args, **kwargs):
    """
    Wrapper around GNU 'ls' with preset settings for \\'one-button\\' usage.
    FILE is a path(s) to directories and files of interest and can be used
    multiple times, default is current/working directory. Runs and formats
    the output of '/bin/ls'. Default format is long, entries are sorted by
    file name, file sizes are in human-readable SI-form. No dereferencing
    is performed by default. Directories are grouped before files.\n\n

    File types indicators ('mc' nomenclature):\n\n

      `   ` regular file       ` | ` pipe              ` = ` socket\n
      ` * ` executable file    ` @ ` symlink to file   ` + ` block device\n
      ` / ` directory          ` ~ ` symlink to dir    ` - ` character device\n\n

    This command requires ++/bin/ls++ to be present and available.
    """
    from es7s.cmd.ls import action

    action(*args, **kwargs)
