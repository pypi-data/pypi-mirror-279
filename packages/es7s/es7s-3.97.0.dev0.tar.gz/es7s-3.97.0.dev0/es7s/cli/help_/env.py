# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import click

from .options import OptionsCliCommand
from .._base import Context, HelpFormatter
from .._base_opts_params import HelpPart
from .._decorators import cli_command, cli_pass_context, catch_and_log_and_exit


class HelpEnvCliCommand(OptionsCliCommand):
    ENVIRONMENT_PROLOG = [
        HelpPart(
            "As a rule of a thumb, a variable defined in the config has "
            "lower priority than *the* *same* variable set up in the environment, and both has lower "
            "priority than a corresponding command line option (if it exists). To sum up:",
            title="Environment",
        ),
        HelpPart(
            "COMMAND LINE OPTION  >  ENVIRONMENT VARIABLE  >  CONFIG VARIABLE", indent_shift=1
        ),
        HelpPart(
            "The only exception is how '--verbose' command line option interacts with monitor "
            "debugging markup setup: because the main purpose of the option is different, it "
            "affects the markup if and only if config variable and environment variable both "
            "are empty, and is ignored in this context otherwise (see below)."
        ),
    ]
    ENVIRONMENT_RO = [
        (
            "ES7S_CLI",
            "Contains path to CLI entrypoint of 'es7s' system.",
        ),
        ("",),
        (
            "ES7S_SHELL_COMMONS",
            "Contains path to es7s/commons legacy shared library for G1/G2 shell components.",
        ),
        ("",),
        (
            "ES7S_THEME_COLOR_SGR",
            "Contains SGR params defining current theme color (config var <general.theme-color>).",
        ),
        ("",),
        (
            "ES7S_USER_REPOS_PATH",
            "Corresponds to config value <general.user-repos-path>. Contains "
            "path to user git repositories dir for various purposes: making "
            "backups, auto-fetching, synchronizing etc. All these background "
            "processes are disabled by default and shall be turned on in the "
            "configuration file.",
        ),
    ]
    ENVIRONMENT_WO = [
        (
            "ES7S_VERBOSITY",
            "Non-empty string determines detail level of the logs (for valid "
            "values see the table above). If the verbosity is set to max level, "
            "extended output of 'pytermor' formatting library is enabled as well (by "
            "setting @PYTERMOR_TRACE_RENDERS@). Works in [CLI] and [GTK] domains, "
            "whereas '-v' or '--trace' options are recognized by CLI entrypoint only. "
            "Note that command line option has a higher priority than an environment "
            "variable.",
        ),
        ("",),
        (
            "ES7S_LOGFILE",
            "Non-empty string with a path to a file for log writing. No file logging is "
            "performed if the variable is missing or empty. Corresponding config "
            "variable: {{@TODO <<general.logfile>>}}.",
        ),
        ("",),
        (
            "ES7S_DAEMON_DEBUG",
            "Non-empty string: ",
        ),
        *[
            ("", s)
            for s in (
                " - makes clients and daemon use different socket server address "
                "for IPC, which helps to avoid conflicts with installed and running "
                "system 'es7s' daemon instance; ",
                " - allows the python debugger to stay connected by keeping "
                "the daemon process attached.",
            )
        ],
        ("", "(Cannot be set via config)"),
        ("",),
        (
            "ES7S_MONITOR_DEBUG",
            "Non-empty string enables CLI monitor output debugging markup. Corresponding "
            "config variable: <monitor.debug>. Is set by tmux, but can also be set "
            "manually, as a regular env var. When both configuration and environment "
            "variable are *unset*, the system uses the current verbosity level to see "
            "if the mode should be enabled, and will do so on `DEBUG` and `TRACE` "
            "verbosity levels.",
        ),
        ("",),
        (
            "ES7S_INDICATOR_DEBUG",
            "Non-empty string enables indicator output debugging markup. Corresponding "
            "config variable: <indicator.debug>.",
        ),
        ("",),
        (
            "ES7S_CLI_ENVVAR",
            "Non-empty string switches the application to special mode which allows setting "
            "command options via environment variables. Corresponding variable names will appear "
            "in the help descriptions of each command."
        ),
        ("", 'Format: "@ES7S_@<<GROUP>>@_@<<COMMAND>>@_@<<OPTION>>"'),
        ("", 'Example: @ES7S_MONITOR_BATTERY_DEMO@'),
        ("",),
        (
            "ES7S_CLI_DEBUG_IO",
            "Non-empty string enables mirroring all data sent to stdout and stderr to temp files "
            "'/tmp/es7s-stdout' and '/tmp/es7s-stderr'. Has the same effect as <cli.debug-io> config "
            "variable, but with higher priority.",
        ),
        ("",),
        (
            "PYTERMOR_*",
            "These variables configure *pytermor*, the library which is used internally for "
            "displaying the formatted text to the terminal. The basic usage and details can "
            "be found in official docs: https://pypi.org/project/pytermor. Any of these "
            "can be set as 'es7s' environment var and will be processed as expected:",
        ),
        ("",),
        *[
            ("", s)
            for s in (
                "⏺ {PYTERMOR_DEFAULT_OUTPUT_MODE}",
                "⏺ {PYTERMOR_FORCE_OUTPUT_MODE}",
                "⏺ {PYTERMOR_PREFER_RGB}",
                "⏺ {PYTERMOR_RENDERER_CLASS}",
                "⏺ {PYTERMOR_TRACE_RENDERS}",
            )
        ],
        ("",),
    ]

    def format_epilog(self, ctx: Context, formatter: HelpFormatter) -> None:
        self._format_help_parts(formatter, self.ENVIRONMENT_PROLOG)

        formatter.write_paragraph()
        formatter.write_heading("Variables set by app", newline=False, colon=False)
        with formatter.indentation():
            formatter.write_dl(self.ENVIRONMENT_RO)

        formatter.write_paragraph()
        formatter.write_heading("Variables set by user", newline=False, colon=False)
        with formatter.indentation():
            formatter.write_dl(self.ENVIRONMENT_WO)


@cli_command(
    name=__file__,
    cls=HelpEnvCliCommand,
    short_help="environment vars that the app reads and writes",
)
@cli_pass_context
@catch_and_log_and_exit
def invoker(ctx: click.Context, **kwargs):
    click.echo(ctx.get_help())
