# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from __future__ import annotations

import functools
import re
import sys
import typing as t
from collections.abc import Iterable
from functools import update_wrapper, partial

import click
import pytermor as pt
from click import Argument
from click.decorators import _param_memo

from es7s.shared import get_logger, get_stderr, exit_gracefully
from es7s.shared.uconfig import get_merged
from ._base import CliGroup, CliCommand
from ._base_opts_params import (
    HelpPart,
    CommandOption,
    CMDTYPE_BUILTIN,
    CommandType,
    EnumChoice,
    DateTimeType,
    SharedOptions,
    IntRange,
    FloatRange,
    OPT_VALUE_AUTO,
)
from es7s.shared.pt_ import Sentinel, condecorator

F = t.TypeVar("F", bound=t.Callable[..., t.Any])
FC = t.TypeVar("FC", bound=t.Union[t.Callable[..., t.Any], click.Command])
FCT = t.Callable[[FC], FC]

_NOT_SET = Sentinel()


def catch_and_log_and_exit(func: F) -> F:
    def wrapper(*args, **kwargs):
        logger = get_logger()
        try:
            logger.debug(f"Entering: '{func.__module__}'")
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            exit_gracefully(exit_code=1)
        except SystemExit as e:
            logger.debug(f"SystemExit: {e.args}")
        else:
            logger.debug(f"Leaving: '{func.__module__}'")
        return func

    return update_wrapper(t.cast(F, wrapper), func)


def catch_and_print(func: F) -> F:
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            if stderr := get_stderr(require=False):
                stderr.echo("ERROR")
            else:
                sys.stderr.write("ERROR\n")
            raise
        return func

    return update_wrapper(t.cast(F, wrapper), func)


def cli_group(
    name: str,
    short_help: str = None,
    epilog: str | HelpPart | list[str | HelpPart] = None,
    autodiscover_extras: "AutoDiscoverExtras" = None,
    **attrs: t.Any,
) -> CliGroup:
    if attrs.get("cls") is None:
        attrs["cls"] = CliGroup
    attrs.setdefault("short_help", short_help)
    attrs.setdefault("epilog", epilog)
    attrs.setdefault("autodiscover_extras", autodiscover_extras)

    return t.cast(CliGroup, click.group(name, **attrs))


def cli_command(
    name: str,
    short_help: str = None,
    import_from: str = None,
    cls: type = CliCommand,
    type: CommandType = CMDTYPE_BUILTIN,
    # shared_opts: SharedOptions = None,
    command_examples: Iterable[pt.RT | Iterable[pt.RT]] = [],
    output_examples: Iterable[pt.RT | Iterable[pt.RT]] = [],
    **attrs: t.Any,
) -> CliCommand:
    attrs.setdefault("import_from", import_from)
    attrs.setdefault("short_help", short_help)
    attrs.setdefault("type", type)
    # attrs.setdefault("shared_opts", shared_opts)
    attrs.update(
        {
            "command_examples": command_examples,
            "output_examples": output_examples,
        }
    )

    cmd = click.command(name, cls, **attrs)
    # if shared_opts:
    #     cmd = add_shared_opts(shared_opts)(cmd)
    return t.cast(CliCommand, cmd)


def _handle_from_config_attr(invoker, attrs: t.Any):
    if n := attrs.pop("from_config", None):
        fb = attrs.get("default", None)

        deferred_load = (
            lambda o=invoker, n=n, fb=fb: get_merged().get_module_section(o).get(n, fallback=fb)
        )
        attrs.update({"default": deferred_load})


def _handle_datetime(attrs: t.Any):
    if (opt_type := attrs.get("type", None)) and isinstance(opt_type, DateTimeType):
        if attrs.get("help") == _NOT_SET:
            attrs.update({"help": opt_type.default_help})
        attrs.setdefault("metavar", opt_type.metavar)


def cli_argument(*param_decls: str, **attrs: t.Any) -> FCT:
    def decorator(f: FC) -> FC:
        _handle_from_config_attr(f, attrs)
        _handle_datetime(attrs)

        ArgumentClass = attrs.pop("cls", None) or Argument
        _param_memo(f, ArgumentClass(param_decls, **attrs))
        return f

    return decorator


def cli_option(*param_decls: str, help: str = _NOT_SET, cls=CommandOption, **attrs: t.Any) -> FCT:
    opt_type = attrs.get("type")

    if isinstance(opt_type, EnumChoice) and opt_type.inline_choices:
        help += opt_type.get_choices_str()
    attrs.setdefault("help", help)

    def decorator(f: FC) -> FC:
        _handle_from_config_attr(f, attrs)
        _handle_datetime(attrs)

        option_attrs = attrs.copy()
        OptionClass = cls or option_attrs.pop("cls", CommandOption)
        try:
            _param_memo(f, OptionClass(param_decls, **option_attrs))
        except AttributeError as e:
            get_logger(require=False).warning(str(e))
        return f

    return decorator


cli_flag = partial(cli_option, is_flag=True)
""" *param_decls, help, cls, **attrs """

cli_pass_context = click.pass_context


_adaptive_input_examples = [
    "1. use arguments as literal input data:",
    "     {} INPUT1 INPUT2...",
    "2. read input data from a file:",
    "     {} -F path/to/file",
    "3. read input data from stdin (e.g. redirected from other command):",
    "     {} -S < <(cmd)",
    "4. read input data from a file first, then from stdin:",
    "     {} -F ./file2 -S",
]
AdaptiveInputAttrs = dict(
    interlog=[
        HelpPart(
            "This command supports @AI unified input interface, which effectively means "
            "that input data can be provided in a several ways (see the examples below):",
            title="Adaptive input:",
        ),
        HelpPart(
            [
                ("INPUT", "as command line arguments if no '-F'/'-S' options are present;"),
                ("FILENAME", "read from file(s) specified with '-F';"),
                ("(STDIN)", "read from standard input if '-S' is specified."),
            ]
        ),
    ],
    command_examples=[*_adaptive_input_examples],
)
AdaptiveInputWithDemoAttrs = AdaptiveInputAttrs.copy()
AdaptiveInputWithDemoAttrs.update(
    {
        "command_examples": [
            *_adaptive_input_examples,
            ("5. use preset demo example as input data:", "   {} -d", ""),
        ]
    }
)


def cli_full_terminal(func):
    @cli_option(
        "-i",
        "--interval",
        type=FloatRange(0.0, max_open=True),
        default=1.0,
        show_default=True,
        help="Delay between frame renderings.",
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def cli_adaptive_input(demo=False, default_stdin=True, input_args=True, null=False, **kwargs):
    """
    :param demo:          If True, '--demo' option is addedl child action is
                          expected to implement get_demo() method.
    :param default_stdin: If True and no -F is provided, read from stdin.
    :param input_args:    If True, use args as input.
    :param null:          If True, the option to split input using '\0' instead
                          of '\n' is provided.
    """

    def decorator(func):
        @condecorator(
            cli_argument("input", metavar="[INPUT]", required=False, nargs=-1), input_args
        )
        @cli_option(
            "-F",
            "--file",
            help=(
                "Discard INPUT arguments, read from FILENAME instead."
                if input_args
                else "Read from FILENAME; can be provided multiple times."
            )
            + " @AI",
            type=click.File(mode="r"),
            multiple=True,
            default=["-"] if default_stdin else [],
        )
        @cli_flag(
            "-S",
            "--stdin",
            help="Read from standard input stream (same as '-F -').",
        )
        @condecorator(
            cli_flag("-d", "--demo", help="Ignore all input options and run on preset example."),
            demo,
        )
        @condecorator(
            cli_option(
                "-0",
                "--null",
                is_flag=True,
                default=False,
                help="Split input values by `0x00` (NUL) byte [default: by \\n].",
            ),
            null,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def cli_multithreaded(**kwargs):
    kwargs.setdefault("type", IntRange(0))
    kwargs.setdefault("default", OPT_VALUE_AUTO)
    kwargs.setdefault("help", "How many threads to use (0=auto).")
    kwargs.setdefault("show_default", True)

    def decorator(func):
        @cli_option("-T", "--threads", **kwargs)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
