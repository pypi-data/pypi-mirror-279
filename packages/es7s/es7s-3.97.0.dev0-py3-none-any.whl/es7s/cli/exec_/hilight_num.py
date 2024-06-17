# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from .._decorators import (
    catch_and_log_and_exit,
    cli_command,
    cli_adaptive_input,
    AdaptiveInputWithDemoAttrs,
)


@cli_command(__file__, "highlight numbers in text", **AdaptiveInputWithDemoAttrs)
@cli_adaptive_input(demo=True)
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Read text from given FILE and highlight all occurrences of numbers with [prefixed] units. Color
    depends on value OOM (order of magnitude). If FILE is omitted or equals to ''-'', read standard
    input instead.\n\n

    Is used by es7s 'ls'.
    """
    from es7s.cmd.hilight_num import action

    action(**kwargs)
