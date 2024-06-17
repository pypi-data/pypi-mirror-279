# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from click import IntRange

from es7s.shared.enum import FilterType, SelectorType
from .._base_opts_params import CMDTRAIT_X11, CMDTYPE_BUILTIN, EnumChoice, HelpPart
from .._decorators import (
    catch_and_log_and_exit,
    cli_argument,
    cli_command,
    cli_option,
    cli_pass_context,
)


@cli_command(
    name=__file__,
    short_help="switch between workspaces",
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_X11],
    epilog=[
        HelpPart(
            "<indexes>=` 0 1 `   <filter>=`whitelist`   <selector>=`first`   workspaces:{0}1 2",
            title="Workflow examples:",
            group="1",
        ),
        HelpPart("< >", group="1"),
        HelpPart(
            "  After hitting the keystroke exclude active workspace from overall list "
            "=> 1 2, apply the whitelist => 1, and switch to the only one available "
            "left, which is *1*. /*This example together with the next one illustrate "
            "how the workspaces can be toggled between each other using one and the "
            "same key combination.*/",
            group="1",
        ),
        HelpPart(
            "<indexes>=` 0 1 `   <filter>=`whitelist`   <selector>=`first`   workspaces: 0{1}2",
            group="2",
        ),
        HelpPart("< >", group="2"),
        HelpPart(
            "  Exclude active from overall => 0 2, apply the whitelist => 0, "
            "and switch to the only one available workspace left, which is *0*. "
            "/*As you can see, this setup implements switching between workspaces "
            "0 and 1, while 2 is ignored.*/",
            group="2",
        ),
        HelpPart(
            "<indexes>=` 3 `   <filter>=`blacklist`   <selector>=`cycle`   workspaces: 0{1}2 3 4",
            group="3",
        ),
        HelpPart("< >", group="3"),
        HelpPart(
            "  Exclude active first => get 0 2 3 4, then subtract blacklisted "
            "and get 0 2 4, then find the leftmost available workspace relative to the "
            "place where our active workspace was originally located, which is *2*."
            "/* The next invocation results in *4*, the one after that -- in *0*, and "
            "so the selector will make one full cycle and can start the next one. */",
            group="3",
        ),
    ],
)
@cli_argument(
    "indexes",
    type=IntRange(0, max_open=True),
    nargs=-1,
)
@cli_option(
    "-f",
    "--filter",
    type=EnumChoice(FilterType),
    from_config="filter",
    help="Name of the filter method to apply to the list of target workspace indexes. If omitted,  "
    "read it from config.",
)
@cli_option(
    "-s",
    "--selector",
    type=EnumChoice(SelectorType),
    from_config="selector",
    help="Name of the selector method used to choose the final workspace to switch to if there "
    "is more than 1 of them. If omitted, read it from config.",
)
@cli_option(
    "-n",
    "--dry-run",
    is_flag=True,
    default=False,
    help="Don't actually switch to other workspace, just pretend to "
    "(suggestion: can be used with '-vv' for debugging).",
)
@cli_option(
    "-S",
    "--shell",
    is_flag=True,
    default=False,
    help="Instead of normal execution create or refresh shell script with hardcoded "
    "current configuration on-board (the values from config can be rewritten "
    "with command args and persist in the shell script till next script update). "
    "Shall be used for invocations instead of calling slow general-purpose 'es7s' "
    "CLI entrypoint (x10 speed boost, from 250ms to 25ms). Optimized entrypoint "
    "is located in @USER_ES7S_BIN_DIR@ environment variable and should be "
    "called directly: 'switch-wspace-turbo'.",
)
@cli_pass_context
@catch_and_log_and_exit
def invoker(*args, **kwargs):
    """
    Switch the current workspace to the next available one. Convenient for a
    situations when you want to have a keystroke to switch the workspaces
    back and forth, but do not want to keep several different key combos for each
    workspace and will be satisfied with just one keystroke that can cycle through
    specified workspace indexes. The algorithm is:\n\n

    - Get current workspace list from the OS, exclude the active workspace from it.\n\n

    - Apply the specified *filter* method to current workspace list with the INDEXES arguments
    as filter operands. In case the filter method is `blacklist`, exclude the INDEXES from
    current workspace list. In case of `whitelist` keep indexes that are present in
    INDEXES list and throw away all the others. Do not perform a filtration if method is set
    to `off`. Note that INDEXES arguments are optional and if the list is omitted, it will be
    read from the config instead.\n\n

    - Pick suitable index from filtered list using *selector* method. In case it is `first`,
    just return the very first element of the list (i.e., the lowest index). In case it is
    `cycle`, the result workspace will be the leftmost workspace in the filtered list after
    the current one, or first if there are none such a workspaces.\n\n

    - Switch the current workspace to the one selected in previous step.\n\n

    This command requires ++/bin/wmctrl++ to be present and available.
    """
    from es7s.cmd.switch_wspace import action

    action(*args, **kwargs)
