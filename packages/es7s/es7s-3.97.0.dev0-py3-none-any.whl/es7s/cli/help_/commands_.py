# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import sys
import typing as t
from typing import cast

import click
import pytermor as pt

from es7s.shared import get_stdout, FrozenStyle
from .._base import (
    CliCommand,
    CliGroup,
    HelpFormatter,
    CliBaseCommand,
    HelpStyles,
)
from .._base_opts_params import CommandAttribute
from .._decorators import cli_pass_context, catch_and_log_and_exit, cli_command, cli_option


@cli_command(
    name=__file__,
    cls=CliCommand,
    short_help="tree of es7s commands",
)
@cli_option(
    "-r/-R",
    "--raw/--no-raw",
    default=None,
    help="disable all formatting in the output and hide the legend ('-r'), or force the formatting and the legend to "
    "be present ('-R'); if output device is not a terminal, '-r' is added automatically (see 'es7s help options' "
    "for the details).",
)
@cli_pass_context
@catch_and_log_and_exit
class invoker:
    """
    Print es7s commands with descriptions as grouped (default) or plain list.
    """

    def __init__(self, ctx: click.Context, raw: bool = None, **kwargs):
        self._raw = raw
        if self._raw is None:
            if not sys.stdout.isatty():
                self._raw = True

        self._formatter = HelpFormatter()

        self._run(ctx)

    def _run(self, ctx: click.Context):
        root_cmd = cast(CliGroup, ctx.find_root().command)

        self._formatter.write_dl(
            [*filter(None, self._iterate([*root_cmd.commands.values()], [root_cmd], []))],
            dynamic_col_max=True,
        )

        print_legend = self._raw is False or self._raw is None
        if print_legend:
            self._formatter.write_paragraph()
            with self._formatter.indentation():
                self._formatter.write_dl([*self._format_legend(root_cmd)])

            self._formatter.write_paragraph()
            with self._formatter.indentation():
                self._formatter.write_dl(
                    [
                        (
                            f'({pt.Fragment("♧", "gray50")}) G1 ',
                            "First shell scripts later partially combined into "
                            "es7s/commons (Nov 21—Apr 22)",
                        ),
                        (
                            f'({pt.Fragment("♢", "gray50")}) G2 ',
                            "Shell/Python scripts as es7s/tmux and leonardo "
                            "components (Apr 22~Nov 22)",
                        ),
                        (
                            f'({pt.Fragment("♠", "gray100")}) G3 ',
                            "Python scripts as parts of centralized es7s " "system (Nov 22+)",
                        ),
                        (
                            f'({pt.Fragment("♥", "gray100")}) G4 ',
                            "Golang applications for bottlenecks where execution "
                            "speed is critical (May 23+)",
                        ),
                    ],
                )
            self._formatter.write_paragraph()
            with self._formatter.indentation():
                self._formatter.write_text(
                    get_stdout().render(
                        pt.Text(
                            "Default command in group, if any, is displayed in ",
                            "italics",
                            pt.Styles.ITALIC,
                            "; a group with such command can be invoked directly.",
                        )
                    )
                )

        result = self._formatter.getvalue().rstrip("\n")
        if self._raw:
            get_stdout().echo_raw(result)
        else:
            get_stdout().echo(result)

    def _format_entry(
        self,
        cmd: CliBaseCommand,
        stack: list[CliBaseCommand | None],
        last_in_group: list[bool],
        cname_st_over: pt.Style = pt.NOOP_STYLE,
    ) -> tuple[str, str] | None:
        stdout = get_stdout()

        is_group = isinstance(cmd, CliGroup)
        cname = [c.name for c in [*stack[1:], cmd]]
        if self._raw:
            return " ".join(cname), ""

        struct = ""
        seen_group = False
        for (idx, p) in enumerate(stack[::-1]):
            struct += ""
            real_idx = len(stack) - idx - 1
            cur_lig = last_in_group[real_idx]
            if not seen_group and isinstance(p, CliGroup):
                if real_idx == 0:
                    struct += "═"
                    struct += "╠╚"[last_in_group[-1]]
                else:
                    struct += "╴"
                    struct += "├└"[last_in_group[-1]]
                seen_group = True
            else:
                struct += "  "
                struct += "│║│ "[(real_idx == 0) | (cur_lig << 1)]

        ctype_str = get_stdout().render(self._formatter.format_command_icon(cmd))
        cname_st_base = cmd.get_command_type().get_name_fmt(False)
        cname_last_st_base = cmd.get_command_type().get_name_fmt(cmd.default_in_group)
        cname_st = pt.merge_styles(cname_st_base, overwrites=[cname_st_over, pt.Style(dim=True)])
        cname_last_st = pt.merge_styles(cname_last_st_base, overwrites=[cname_st_over])
        cname_str = (
            stdout.render(" ".join(cname[:-1]), cname_st)
            + " "
            + stdout.render(cname[-1], cname_last_st)
        )
        left_col = (
            struct[::-1]
            + ["", "["][is_group]
            + ctype_str
            + ["", "]"][is_group]
            + " "
            + cname_str.strip()
        )

        right_col = ""
        if not is_group:
            right_col = cmd.get_short_help_str()

        return left_col, right_col

    def _format_command(
        self,
        cmd: CliBaseCommand,
        stack: list[CliBaseCommand | None],
        last_in_group: list[bool],
    ) -> tuple[str, str] | None:
        return self._format_entry(cmd, stack, last_in_group)

    def _format_group(
        self, cmd: CliBaseCommand, stack: list[CliBaseCommand | None], last_in_group: list[bool]
    ) -> tuple[str, str] | None:
        return self._format_entry(
            cmd, stack, last_in_group, FrozenStyle(HelpStyles.TEXT_HEADING, bold=True)
        )

    def _iterate(
        self,
        cmds: t.Iterable[CliBaseCommand],
        stack: list[CliBaseCommand | None],
        last_in_group: list[bool],
    ):
        scmds = [*sorted(cmds, key=lambda c: c.name)]
        for (idx, cmd) in enumerate(scmds):
            local_last_in_group = last_in_group + [idx == len(scmds) - 1]
            if not isinstance(cmd, CliGroup):
                yield self._format_command(cmd, stack, local_last_in_group)
            else:
                yield self._format_group(cmd, stack, local_last_in_group)
                yield from self._iterate(
                    cmd.get_commands().values(),
                    stack + [cmd],
                    local_last_in_group,
                )

    def _format_legend(self, root_cmd: CliGroup) -> tuple[str, str]:
        prev = None
        for ct in sorted(CommandAttribute.values(), key=lambda el: el.sorter):
            if ct.hidden:
                continue
            fmtd = self._formatter.format_command_attribute_legend(ct)
            try:
                desc = ct.description % ""
            except TypeError:
                desc = ct.description

            if prev and type(prev) != type(ct):
                yield "", ""
            prev = ct

            yield get_stdout().render(fmtd), desc.replace("|", " ").replace("  ", " ")
