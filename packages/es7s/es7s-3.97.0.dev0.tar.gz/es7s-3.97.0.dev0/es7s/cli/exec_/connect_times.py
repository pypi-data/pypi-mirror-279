# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from .._base_opts_params import IntRange, CMDTRAIT_ADAPTIVE_OUTPUT
from .._decorators import cli_command, cli_argument, cli_option, catch_and_log_and_exit


@cli_command(
    __file__, "measure connect timings (lookups, redirects)", traits=[CMDTRAIT_ADAPTIVE_OUTPUT]
)
@cli_argument("url", type=click.STRING, required=True, nargs=-1)
@cli_option(
    "-p",
    "--proxy",
    metavar="[protocol://]host[:port]",
    default=None,
    help="Use the specified proxy. 'protocol' is one of: `http` [is a default], "
    "`https`, `socks4`, `socks4a`, `socks5`, `socks5h`. If not specified, the 'port' is "
    "1080. Proxy auth should work as well, to use it provide credentials in the form of "
    '""username:password@host"" instead of just ""host"" alone.',
)
@cli_option(
    "-x",
    "--extend",
    count=True,
    help="Increase the amount of details. Can be used multiple times ('-xx', "
    "'-xxx'). The first level enables detailed event log output, the second enables "
    "tracing requests and responses as text, the third -- same, but as bytes instead.",
)
@cli_option(
    "-w",
    "--width",
    default=40,
    show_default=True,
    type=IntRange(_min=10, max_open=True),
    help="Output scale width, in characters.",
)
@catch_and_log_and_exit
def invoker(*args, **kwargs):
    """
    Perform a HTTP request of the given URL(s) and measure connection timings of
    each attempt:\n\n

        ⏺ \\"DNS lookup\\"\n
        ⏺ \\"Connect\\"\n
        ⏺ \\"App connect\\"\n
        ⏺ \\"Pre-transfer\\"\n
        ⏺ \\"Redirectons\\"\n
        ⏺ \\"Start transfer\\"\n\n

    Requires ++curl++. @A> Adjusts the output depending on a terminal size.
    """
    from es7s.cmd.connect_times import action

    action(*args, **kwargs)
