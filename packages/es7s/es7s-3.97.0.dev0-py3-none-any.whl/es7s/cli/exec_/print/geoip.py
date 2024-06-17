# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from ..._base_opts_params import IpParamType
from ..._decorators import catch_and_log_and_exit, cli_argument, cli_command


@cli_command(__file__, "get associated country for IP address")
@cli_argument("ADDRESS", type=IpParamType(), required=False)
@catch_and_log_and_exit
class invoker:
    """
    Display the country bound to specified IP 'ADDRESS'.
    """

    def __init__(self, **kwargs):
        from es7s.cmd.print_geoip import action
        action(**kwargs)
