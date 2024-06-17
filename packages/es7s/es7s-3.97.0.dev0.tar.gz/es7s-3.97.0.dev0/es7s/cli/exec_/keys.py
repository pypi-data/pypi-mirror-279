# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from .._base_opts_params import CMDTRAIT_X11, EnumChoice, HelpPart
from .._decorators import catch_and_log_and_exit, cli_command, cli_flag, cli_argument
from es7s.shared.enum import KeysMode


keys_choice = EnumChoice(KeysMode, inline_choices=True)


@cli_command(
    __file__,
    "display key bindings",
    traits=[CMDTRAIT_X11],
    interlog=[
        HelpPart(
            "Valid values:  " + ", ".join(keys_choice.choices),
            title="Subjects:",
        )
    ],
)
@cli_argument("subject", type=keys_choice, nargs=-1, required=False)
@cli_flag("-a", "--all", help="Display all subjects.")
@cli_flag("-d", "--details", help="Include bind commands and other details.")
@cli_flag("-g", "--group", help="Display subject bindings semantically grouped (when applicable).")
@cli_flag("-t", "--sort-by-title", help="Sort bindings by title [default: by key sequence].")
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Get a list of current key bindings, format it and display. Intended to run as
    a tmux popup, but can be invoked directly as well.
    """
    from es7s.cmd.keys import action

    action(**kwargs)
