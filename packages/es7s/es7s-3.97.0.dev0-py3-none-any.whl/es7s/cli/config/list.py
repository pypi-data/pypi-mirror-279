# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023-2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from .._decorators import cli_command, catch_and_log_and_exit


@cli_command(name=__file__, short_help="display user/default config variables with values")
@catch_and_log_and_exit
class invoker:
    """
    Display merged config variables values. The values that differ from the default
    (i.e. altereed by user) are colored with blue and green, while the variables with
    a default value are gray/white.\n\n

    Common option '--default' can be used to ignore user config and limit the list
    with the default variable values.
    """

    def __init__(self):
        from es7s.cmd.config import action_list as action
        action()
