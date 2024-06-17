# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from ..._decorators import cli_command
from ..._decorators import cli_option


@cli_command(__file__, "network interface list")
@cli_option('-H', '--no-header', is_flag=True, help='Omit header from the output.')
class invoker:
    """
    DIsplay a list of network interfaces with properties.
    """
    def __init__(self, **kwargs):
        from es7s.cmd.print_netifs import action
        action(**kwargs)
