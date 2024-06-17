# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re
from dataclasses import dataclass
from functools import cached_property
from math import floor
from typing import cast

import click
import pytermor as pt
from es7s_commons import NamedGroupsRefilter
from pytermor import PTT, FT

from .._base import Context, HelpFormatter, CliCommand
from .._base_opts_params import HelpPart, CommandType, CommandAttribute
from .._decorators import (
    cli_command,
    cli_pass_context,
    catch_and_log_and_exit,
    cli_option,
    cli_flag,
)
from ...shared import get_stdout, Styles


@dataclass(frozen=True)
class Element:
    title: str
    syntax: str | None
    example: str
    desc: str
    fixed: bool = False
    _spaces_in_raw: bool = None
    _spaces_in_fmtd: bool = None

    @cached_property
    def spaces_in_raw(self) -> bool:
        if self._spaces_in_raw is None:
            return self.fixed
        return self._spaces_in_raw

    @cached_property
    def spaces_in_fmtd(self) -> bool:
        if self._spaces_in_fmtd is None:
            return self.fixed
        return self._spaces_in_fmtd


class HelpPrimerCliCommand(CliCommand):
    PRIMER_EPILOG = [
        HelpPart(
            [
                Element(
                    "Header",
                    "{{VAL}}",
                    "{{SYNOPSIS}}",
                    "Yellow bold, CAPS if element is at start of the line.",
                ),
                Element(
                    "Default value",
                    "[default: VAL]",
                    "[default: 1]",
                    "Default option value highlight, search for '[default: *]' construction is performed.",
                ),
                Element(
                    "I/O example I",
                    "`VAL`",
                    "`4 11`",
                    "Input or output value example. The characters are [U+60 GRAVE ACCENT]. Can also be used for styling "
                    "enumerations.",
                ),
                Element(
                    "I/O example II",
                    "´VAL´",
                    "´4 11´",
                    "Input or output value example (◆ static/fixed version). Always occupies as many characters as it does in the source text. "
                    "The characters are [U+B4 ACUTE ACCENT]",
                    fixed=True,
                ),
                Element(
                    "Command type",
                    "[[VAL]]",
                    "[[builtin]]",
                    "Badge with a colored command type char icon and name.\n\nValid values: "
                    + " , ".join(
                        [
                            *[
                                "[[" + ct.name + "]]"
                                for ct in sorted(CommandType.values(), key=lambda ct: -ct.sorter)
                                if not ct.hidden and isinstance(ct, CommandType)
                            ]
                        ],
                    ),
                ),
                Element(
                    "Command trait",
                    "@VAL",
                    "@AI",
                    "Colored icon of command attribute.\n\nValid values: "
                    + " , ".join(
                        [
                            *[
                                " @" + ct.abbr + " " + ct.abbr
                                for ct in sorted(
                                    CommandAttribute.values(), key=lambda ct: ct.sorter
                                )
                                if not ct.hidden and ct.abbr and isinstance(ct, CommandAttribute)
                            ]
                        ]
                    ),
                ),
                Element(
                    "Keyboard key",
                    "&[VAL]",
                    "&[F10]",
                    "Reference to a keyboard key, value string allowed format is [\w\d_]+ .",
                ),
                Element(
                    "Environment variable name I",
                    "@VAL@",
                    "@ES7S_LE_VAR@",
                    "Green text with an environment variable name, which should consist of [A-Z0-9_] .",
                ),
                Element(
                    "Environment variable name II",
                    "{VAL}",
                    "{ES7S_LE_VAR}",
                    "Green text with an environment variable name (fixed).",
                    fixed=True,
                ),
                Element(
                    "Environment variable name III",
                    "env var: VAL",
                    "env var: ES7S_LE_VAR",
                    "Green text with an environment variable name. Searching is performed for 'env var:' substring.",
                ),
                Element(
                    "Badge",
                    "::VAL::",
                    "::NOTE::",
                    "Label enclosed in blue rectangle.",
                    fixed=True,
                ),
                Element(
                    "Dependency / requirement",
                    "++VAL++",
                    "++gmic++",
                    "Red-colored text, suggested usage is for binary dependencies.",
                ),
                Element(
                    "Config var path (absolute)",
                    "<VAL>",
                    "<section.opt>",
                    "Display magenta-colored full path to a config variable.",
                ),
                Element(
                    "Config var path (relative)",
                    "<~VAL>",
                    "<~opt>",
                    "Display path to a config variable consisting of two parts: left gray base config path, shared with other "
                    "variables in current python file, and right magenta local path. In order to work an option 'import_from' "
                    "should be defined in a CliCommand definition.",
                ),
                Element(
                    "Placeholder",
                    "<<VAL>>",
                    "<<filename>>",
                    "Gray dimmed text enclosed in angle brackets.",
                ),
                Element("Alternative", "^VAL^", "^ALTERNATIVE^", "Italic text.", fixed=True),
                Element(
                    "Comment I",
                    "// VAL",
                    "// COMMENT",
                    "Gray dimmed text from the start of the element to end of the line. One space after slashes is required.",
                ),
                Element(
                    "Comment II",
                    "/* VAL */",
                    "/* COMMENT */ TEXT ",
                    "Gray dimmed text between the boundaries. Spaces between asteriks and string value are required.",
                ),
                Element(
                    "Block",
                    None,
                    "░░░░░░░░",
                    "Gray-colored block of [U+2591 LIGHT SHADE] characters of arbitrary length.",
                ),
                Element(
                    "Abbrev (single)",
                    "&V",
                    "ab&pe",
                    "Underlines a character after an ampersand. Suggested usage is "
                    "abbreviation origins visualizing.",
                ),
                Element(
                    "Abbrev (multi)",
                    "&(VAL)",
                    "f&(gre)p",
                    "Underlines all characters between parentheses.",
                ),
                Element(
                    "Literal",
                    "'VAL'",
                    "'ls | cat -n'",
                    "Recognizes options by '-'/'--', one-char pipe builtins (e.g. pipe symbol |), and "
                    "es7s commands, and uses white bold style, regular bold style and blue fg style "
                    "correspondingly. All other words are considered literal input examples and are styled with "
                    "an underline.",
                ),
                Element(
                    "Literal words",
                    "'VAL'",
                    "'/usr/bin/ls cat'",
                    "Attempts to underline all words in the string value, keeping spaces' styles "
                    "unchanged.",
                ),
                Element(
                    "Accent I",
                    "*VAL*",
                    "*word* *--option*",
                    "Renders specified string(s) with a bold white fg style. Whitespaces "
                    "and [0x1B ESCAPE] are not allowed inside.",
                ),
                Element(
                    "Accent II",
                    '"*VAL*"',
                    '"word" "--option"',
                    "Same as Accent I, but size is fixed.",
                    fixed=True,
                ),
                Element(
                    "Accent III",
                    '""VAL""',
                    '""option""',
                    "Same as Accent I, but with keeping a pair of quotes around the string.",
                ),
                Element(
                    "Accent IV",
                    "“VAL”",
                    "“*ON/OFF+”",
                    "Bold and underlined, suggested usage is " "for key terms / definitions.",
                ),
                Element(
                    "Plain I",
                    r"\'VAL\'",
                    r"\'text\'",
                    "Plain unstyled text. Quotes are kept.",
                ),
                Element(
                    "Plain II",
                    r"\"VAL\"",
                    r"\"text\"",
                    "Same as Plain I.",
                ),
                Element(
                    "URL",
                    None,
                    "https://github.com",
                    "Render URLs as gray text with blue underline (some terminal emulators can "
                    "override hyperlink styles with their own, though).",
                ),
            ]
        )
    ]

    # *important* │ *…* │ words            shrinked       # noqa
    #  '--option' │ '…' │ options format   shrinked       # noqa
    #  "--option" │ "…" │                  any* expanded  # noqa
    #  ""option"" │""…""│ -> 'option'      any* fixed     # noqa
    #  \'text\'   │\'…\'│ -> plain 'text' w/o formatting  # noqa
    #  \"text\"   │\'…\'│ -> plain "text" w/o formatting  # noqa

    def format_help_text(self, ctx: Context, formatter: HelpFormatter) -> None:
        pass

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        pass

    def format_options(self, ctx: Context, formatter: HelpFormatter):
        pass

    def format_epilog(self, ctx: Context, formatter: HelpFormatter) -> None:
        stdout = get_stdout()

        max_width = min(80, pt.get_terminal_width(pad=0))
        margin = pt.pad(5)
        body_width = max_width - len(margin) * 2 - 2
        left_width = max_width // 2
        short = ctx.params.get("short")

        for hp in self.PRIMER_EPILOG:
            for element in hp.text:
                element: Element
                title = pt.cut(element.title, left_width)
                example = pt.cut(element.example, left_width)
                syntax = pt.Text(width=left_width)
                syntax += (
                    pt.Text(
                        *zip(
                            [*re.split(r"(VAL|V)", element.syntax, 2)],
                            (Styles.DEBUG_SEP_INT, Styles.WARNING, Styles.DEBUG_SEP_INT),
                        )
                    )
                    if element.syntax
                    else pt.Fragment("(auto)", Styles.TEXT_LABEL)
                )
                example_fmtd = formatter._postprocess(example)
                if element.spaces_in_raw:
                    example = SpaceVisualizer.apply(example)
                if element.spaces_in_fmtd:
                    example_fmtd = SpaceVisualizer.apply(example_fmtd)

                """  ┌ ┬ ┐ ├ ┼ ┤  ─ ░ │ ░░╴░╶░░╷░╵░ └ ┴ ┘ """

                lendiff = len(pt.EscSeqStringReplacer().apply(example_fmtd)) - len(element.example)
                if lendiff != 0:
                    lendiff_str = pt.Fragment(f"{lendiff:d}", Styles.MSG_FAILURE)
                else:
                    lendiff_str = pt.Fragment("same", Styles.TEXT_DEFAULT)

                header_line = pt.center_sgr(
                    get_stdout().render(
                        pt.Fragment(" " + title.upper() + " ", pt.Style(inversed=True))
                    ),
                    body_width,
                    "─",
                )
                if not short:
                    header_line = f"{margin}┌{header_line}┐{margin}"
                attr_lines = [
                    pt.Fragment(" fmt", Styles.TEXT_LABEL) + " │ " + syntax,
                    pt.Fragment(" src", Styles.TEXT_LABEL) + " │ " + example,
                    pt.Fragment(" out", Styles.TEXT_LABEL) + " │ " + example_fmtd,
                    pt.Fragment(" len", Styles.TEXT_LABEL) + " │ " + lendiff_str,
                ]
                all_lines = [header_line, *attr_lines]
                if not short:
                    footer_line = f"{margin}└" + ("─" * body_width) + f"┘{margin}"
                    desc = pt.wrap_sgr(
                        formatter._postprocess(element.desc),
                        indent_first=len(margin) + 2,
                        indent_subseq=len(margin) + 2,
                        width=body_width,
                    )
                    all_lines += [footer_line, desc.rstrip(), ""]

                for line in all_lines:
                    stdout.echo_rendered(line)
        return


SpaceVisualizer = pt.StringMapper({0x20: "␣"})


@cli_command(
    name=__file__,
    cls=HelpPrimerCliCommand,
    help="&Not-&Worst-&Markup-&Language specification and examples",
)
@cli_pass_context
@catch_and_log_and_exit
def invoker(ctx: click.Context, **kwargs):
    click.echo(ctx.get_help())
