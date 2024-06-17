from ..._decorators import cli_command, catch_and_log_and_exit


@cli_command(__file__, "ansi &escape &se&quences classifier")
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    // Early experiment (one of) in templating and functional programming (note the one and only print()).
    """
    from es7s.cmd.print_esq_breakdown import action
    action(**kwargs)
