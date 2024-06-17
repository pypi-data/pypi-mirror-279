# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023-2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from .._base_opts_params import IntRange, CMDTRAIT_ADAPTIVE_INPUT, OPT_VALUE_AUTO
from .._decorators import (
    cli_command,
    catch_and_log_and_exit,
    cli_option,
    cli_flag,
    cli_multithreaded,
    cli_adaptive_input,
    AdaptiveInputAttrs,
)


@cli_command(
    __file__,
    short_help="&(fu)sion-&(dra)in &parallel-&processing, remote GAN interface",
    traits=[CMDTRAIT_ADAPTIVE_INPUT],
    **AdaptiveInputAttrs,
)
@cli_adaptive_input()
@cli_multithreaded()
@cli_option(
    "-n",
    "--times",
    help="How many generations to run for each prompt line.",
    type=IntRange(1),
    default=1,
    show_default=True,
)
@cli_option(
    "-r",
    "--retries",
    help="How many times each *failed* generation should be retried.",
    type=IntRange(0),
    default=OPT_VALUE_AUTO,
    show_default=True,
)
@cli_flag("-R", "--no-retry", help="Do not retry failed generations.")
@cli_option(
    "-s",
    "--style",
    help="Picture style. List of supported styles is queried from the remote every time and "
    "is displayed when running with '-v' or when invalid style name is specified.",
    default="DEFAULT",
    show_default=True,
)
@cli_flag(
    "-a",
    "--all-styles",
    help="Each specified prompt will be requested to be made in every available style. Overrides "
    "'-s' option.",
)
@cli_option(
    "-w",
    "--width",
    help="Target image width, in pixels.",
    type=IntRange(128, 1024, clamp=True),
    default=1024,
    show_default=True,
)
@cli_option(
    "-h",
    "--height",
    help="Target image height, in pixels.",
    type=IntRange(128, 1024, clamp=True),
    default=1024,
    show_default=True,
)
@cli_flag(
    "-D",
    "--delete",
    help="Delete image origins (default: keep both the originals and merged composite).",
)
@cli_flag(
    "-M",
    "--no-merge",
    help="Do not merge results into one tiled image, implies '--no-open'. Enabling this option "
    "together with '-D' leads to discarding all the images.",
)
@cli_flag("-O", "--no-open", help="Do not call 'xdg-open' for merged result.")
@catch_and_log_and_exit
class invoker:
    """
    Query a remote service with 'INPUT's (or prompts) describing what should be on the
    picture, wait for completion and fetch the result. If a word starts with
    a hyphen \\"-\\", it is treated like 'negative' prompt. Several arguments
    in quotes are treated as a single prompt, unless there are newlines:\n\n

        fudrapp \\"Prompt number one\\" \\"still same prompt\\"\n\n

        fudrapp $\\'Prompt number one\\n prompt number two\\'\n\n

    Total amount of result pictures is *P*×*T*, where *P* is prompts amount,
    and *T* is '--times' option argument (1 if omitted). Argument of
    '--threads' option does not influence picture amount, rather it controls
    how many jobs will be executed in parallel. If not specified, thread amount
    is set to 2×*Cₗ*, where *Cₗ* is the amount of logical CPU cores in the system
    (running more than *Cₗ* threads still speeds things up, as almost 100% of the
    time threads are just waiting for the responses from the remote).\n\n

    There is an embedded retry mechanism, which queries the same prompt
    several times if the service answers with a placeholder and "'censored'"
    flag, or just fails with an error; retrying can be switched off with
    '--no-retry' flag, or adjusted with '--retries' option. Therefore, maximum
    generation request amount *Ĝ* = *P*×*T*×(*R̂*+1), where *R̂* is retry amount with
    default value equal to *R̂* = max(0, 5 - ceil(log₂(*P*×*T*))):\n\n

     out pictures  *P*×*T* |  1   2  3-4  5-8  9-16  >16 \n
     max retries     *R̂* |  5   4    3    2     1    0  \n
     max requests    *Ĝ* |  6  10  ≤16  ≤24   ≤32  *P*×*T*\n\n

    After the results has been received, they go through a pipeline:\n\n

        1. Combine received results into image in array-like pattern;

        2. Add a label with a prompt line to the bottom of merged image;

        3. Open merged [and labeled] image in an image viewer.\n\n

    The whole pipeline can be disabled with '--no-merge' option; step (2) can be
    disabled using '--no-label'; step (3) can be disabled with '--no-open'. Also
    note that step (3) is always disabled if the application is running outside
    of X11 environment.\n\n

    Remote service is https://fusionbrain.ai. Requires ++gmic++ for image merging.
    {{@TODO fallback to PIL}} \n
    """

    def __init__(self, **kwargs):
        from es7s.cmd.fudrapp import action

        action(**kwargs)
