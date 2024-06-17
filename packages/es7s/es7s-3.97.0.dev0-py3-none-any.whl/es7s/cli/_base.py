# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import inspect
import re
import typing as t
from collections.abc import Iterable
from contextlib import contextmanager
from os.path import basename, dirname, splitext
from re import compile
from typing import ClassVar, cast, overload, TypeVar

import Levenshtein  # noqa (not listed in requirements)
import click
import pytermor as pt
from es7s_commons import Regex, URL_REGEX, format_attrs, NamedGroupsRefilter
from pytermor import PTT, FT, RT

from es7s import APP_NAME
from es7s.shared import (
    FrozenStyle,
    Styles,
    get_logger,
    get_stdout,
    LoggerSettings,
    uconfig,
)
from es7s.shared.uconfig import UserConfigSection
from ._base_opts_params import (
    CMDTRAIT_NONE,
    CMDTYPE_BUILTIN,
    CMDTYPE_GROUP,
    CommandAttribute,
    CommandTrait,
    CommandType,
    EPILOG_ARGS_NOTE,
    EPILOG_COMMAND_HELP,
    EPILOG_COMMON_OPTIONS,
    HelpPart,
    OptionScope,
    Section,
    ScopedOption,
    CMDTYPE_EXTERNAL,
    CMDTYPE_INTEGRATED,
    EPILOG_COMMANDS_TREE,
)

FS = FrozenStyle

LIST_CHAR = "⏺"


class base_invoker:
    @staticmethod
    @overload
    def uconfig(origin) -> UserConfigSection:
        ...

    @classmethod
    @overload
    def uconfig(cls) -> UserConfigSection:
        ...

    def uconfig(self) -> UserConfigSection:
        return uconfig.get_for(self)


InvokerT = TypeVar("InvokerT", bound=base_invoker)


# fmt: off
class HelpStyles(Styles):
    TEXT_HEADING = FS(fg=pt.cv.YELLOW, bold=True)          # {{SYNOPSIS}}  │{{…}}│ also used by help formatter     # noqa
    TEXT_HEADING_REF = FS(fg=pt.cv.YELLOW)                 # {{Synopsis}}  │{{…}}│ if not at start of the line     # noqa
    TEXT_COMMAND_NAME = FS(fg=pt.cv.BLUE)                  # es7s exec     │     │ auto-detection                  # noqa
    TEXT_OPTION_DEFAULT = FS(fg=pt.cv.HI_WHITE, bold=True) # [default: 1]  │ […] │ requires wrapping in [ ]        # noqa
    TEXT_EXAMPLE = FS(fg=pt.cv.CYAN, bg=pt.cv.GRAY_0)      # `4 11`        │ `…` │ input/output example            # noqa
                                                           # ´4 11´        │ ´…´ │ ⤒ static-length I/O example     # noqa
                                                           # [[builtin]]   │[[…]]│ command type inlined            # noqa
                                                             # [[@4]]      │[[@]]│ command type abbrev inlined     # noqa
    TEXT_KEY_PRESS = FS(fg=pt.cv.CYAN, bold=True)          # &[F10]        │ &[…]│ key label                       # noqa
    TEXT_ENV_VAR = FS(fg=pt.cv.GREEN)                      # @ES7S_LE_VAR@ │ @…@ │ environment variable name       # noqa
                                                           # {ES7S_LE_VAR} │ {…} │ ⤒ static-length env var name    # noqa
                                                           # (env var: ..) │     │ requires 'env var:' prefix      # noqa
    TEXT_ABOMINATION = FS(pt.Style(bg='blue').autopick_fg()) # ::NOTE::    │::…::│ needs to be wrapped in ::       # noqa
    TEXT_DEPENDENCY = FS(fg=pt.cv.RED, underlined=True)    # ++REQ++       │++…++│ ++required dependency++         # noqa
    TEXT_INLINE_CONFIG_VAR = FS(fg=pt.cv.MAGENTA,bold=True)# <section.opt> │ <…> │ config variable name            # noqa
    TEXT_PLACEHOLDER = FS(italic=True, dim=True)           # <<filename>>  │<<…>>│ placeholder                     # noqa
    TEXT_ALTER_MODE = FS(italic=True)                      # ^ALT MODE^    │ ^…^ │ alt monitor mode                # noqa
    TEXT_COMMENT = FS(fg=pt.cv.GRAY)                       # // COMMENT    │ //… │ till end of the line            # noqa
    TEXT_WALL = FS(fg=pt.cv.WHITE)                         # ░░░░░░░░      │ ░░░ │ "░" char in tables              # noqa
    TEXT_ABBREV_SINGLE = FS(underlined=True)               # &p &(gre)p    │ &…  │ highlighed part of abbrev       # noqa
    TEXT_ABBREV_MULTI = TEXT_ABBREV_SINGLE                 #               │ &(…)│ highlighed part of abbrev       # noqa
    TEXT_ARGUMENT = FS(underlined=True)                    # FILE ARGUMENT │ ABC │ caps auto-detection             # noqa
    TEXT_LITERAL = FS(bold=True)                           # 'ls | cat'    │ '…' │ non-es7s commands (punctuation) # noqa
    TEXT_LITERAL_WORDS = FS(underlined=True)               # 'ls | cat'    │ '…' │ non-es7s commands (words)       # noqa
    TEXT_ACCENT = FS(bold=True, fg=pt.cv.GRAY_100)         # *important*   │ *…* │ words            shrinked       # noqa
                                                             #  '--option' │ '…' │ options format   shrinked       # noqa
                                                             #  "--option" │ "…" │                  any* expanded  # noqa
                                                             #  ""option"" │""…""│ -> 'option'      any* fixed     # noqa
                                                             #  \'text\'   │\'…\'│ -> plain 'text' w/o formatting  # noqa
                                                             #  \"text\"   │\'…\'│ -> plain "text" w/o formatting  # noqa
    TEXT_KEY_TERM = FS(bold=True, underlined=True)         #  “*ON/OFF+”   │ “…” │ ACCENTED ACCENT, any* shrinked  # noqa
    TEXT_URL = FS(fg=pt.cv.GRAY_50,                        #  https://...  │     │ auto-detection                  # noqa
                  underline_color=pt.Color256.get_by_code(4),    # =BLUE, remove after updating pytermor to 2.212  # noqa
                  underlined=True)


# fmt: on


class NWMarkup:  # @REFACTOR ME  ●︿●
    """
    .. todo::

        This is starting to be a bit too complex and hard to maintain. Applying
        the regular expressions consequently works, but this approach makes it
        difficult to implement e.g. NO-FORMAT tags or something like this.

        Also its quite ineffective because the text is processed a lot of times
        (by a number of filters to apply) over and over again.

        One possible solution is to rewrite this from regex-oriented approach
        to lexer-oriented one, i.e. parse the input string ONCE, split it up
        into _tokens_ depending on the formatting, and then apply styling to
        each token.

    """

    OPTION_REGEX = Regex(R"(?P<val>--?[\w-]+)")

    # language=regexp
    WRAP_RE = R"(\n\s*)?"

    PROCESSED_SEGMENT_START = "\U0010E576"
    PROCESSED_SEGMENT_END = "\U0010E577"
    PROCESSED_SEGMENT_REGEX = Regex(
        Rf"{PROCESSED_SEGMENT_START}(.+?){PROCESSED_SEGMENT_END}", dotall=True
    )

    class RenderingNamedGroupsRefilter(NamedGroupsRefilter):
        def __init__(self, pattern: PTT[str], repl_map: dict[str, FT | RT]):
            super().__init__(pattern, repl_map, renderer=get_stdout().renderer)

        def _render(self, v: pt.RT, repl: FT | RT) -> str:
            if pt.is_rt(repl):
                return repl.render()
            return self._renderer.render(v, repl)

    class RenderingValGroupRefilter(RenderingNamedGroupsRefilter):
        def __init__(self, pattern: pt.filter.PTT[str], val_st: FT):
            super().__init__(pattern, {"val": val_st})

    class InlineConfigVarReplacer(RenderingNamedGroupsRefilter):
        def __init__(self, import_from: str = None):

            super().__init__(
                Regex(Rf"(?<!<)<{NWMarkup.WRAP_RE}(?P<imp>~)?(?P<val>[\w\s.~-]+?)>"),
                {
                    "val": HelpStyles.TEXT_INLINE_CONFIG_VAR,
                    "imp": pt.Fragment(
                        import_from,
                        pt.FrozenStyle(HelpStyles.TEXT_DEFAULT, dim=True),
                    ),
                },
            )

    class CommandTypeReplacer(pt.StringReplacer):
        def __init__(self):
            self.COMMAND_TYPE_NAME_MAP: t.Dict[str, CommandAttribute] = dict()
            self.COMMAND_TYPE_ABBR_MAP: t.Dict[str, CommandAttribute] = dict()
            for ct in CommandAttribute._values:
                if ct.name:
                    self.COMMAND_TYPE_NAME_MAP[ct.name.lower()] = ct
                if ct.abbr:
                    self.COMMAND_TYPE_ABBR_MAP[ct.abbr.upper()] = ct

            names = "|".join(self.COMMAND_TYPE_NAME_MAP.keys())
            abbrs = "|".join(self.COMMAND_TYPE_ABBR_MAP.keys())
            regex = rf"\[\[({names})\]\]|@({abbrs}\b)"

            super().__init__(regex, self.replace)

        def replace(self, m: t.Match) -> str:
            icon_only = m.group(2)
            if icon_only and (ct := self.COMMAND_TYPE_ABBR_MAP.get(icon_only, None)):
                result = HelpFormatter.format_command_type_inlined(ct, True)
                return get_stdout().render(result)
            if ct := self.COMMAND_TYPE_NAME_MAP.get(m.group(1), None):
                result = HelpFormatter.format_command_type_inlined(ct)
                return get_stdout().render(result)
            return m.group()

    class LiteralReplacer(pt.StringReplacer):
        def __init__(self):
            super().__init__(
                Regex(Rf"(?<!\\)'{NWMarkup.WRAP_RE}([\w./ \n|=-]+?)'"),
                self.replace,
            )

        @classmethod
        def replace(cls, sm: re.Match) -> str:
            text_literal_is_present = False
            word_count = 0

            def replace_literal(wm: re.Match) -> str:
                nonlocal text_literal_is_present, word_count
                word_count += 1
                word = wm.group()
                if len(word) < 2 and not word.isalpha():  # bold instead of underline
                    text_literal_is_present = True  # for 1-character non-letters,
                    style = HelpStyles.TEXT_LITERAL  # e.g. for '|' pipe symbol.
                elif word in HelpFormatter.command_names or word.startswith(APP_NAME):
                    style = HelpStyles.TEXT_COMMAND_NAME
                elif word.startswith("-"):
                    style = HelpStyles.TEXT_ACCENT
                else:
                    text_literal_is_present = True
                    style = HelpStyles.TEXT_LITERAL_WORDS
                return get_stdout().render(word, style)

            replaced = re.sub(r"(\S+)", replace_literal, (sm.group(1) or "") + sm.group(2))
            if text_literal_is_present and word_count > 1:
                replaced = f"'{replaced}'"
            return replaced

    def __init__(self, import_from: str = None):
        import_from = (import_from or "").removeprefix(APP_NAME + ".") + "."

        self._filters: t.List[pt.StringReplacer] = [
            # -------------------------------------
            # (-2) {{HEADER_NAME}}   (at start of the line)
            self.RenderingValGroupRefilter(
                Regex(Rf"(\n\s*)\{{\{{{self.WRAP_RE}(?P<val>.+?)}}}}"),
                HelpStyles.TEXT_HEADING,
            ),
            #                        (not at start of the line)
            self.RenderingValGroupRefilter(
                Regex(Rf"\{{\{{{self.WRAP_RE}(?P<val>.+?)}}}}"),
                HelpStyles.TEXT_HEADING_REF,
            ),
            # -------------------------------------
            # [ 0] &[KEY]
            self.RenderingValGroupRefilter(
                Regex(Rf"&(\[)(?P<val>[\w\d_]+)(])"),
                HelpStyles.TEXT_KEY_PRESS,
            ),
            # -------------------------------------
            # [ 0] env var: ENVIRONMENT_VAR
            self.RenderingValGroupRefilter(
                Regex(Rf"(env\n?\s*var:)(\n?\s*)(?P<val>[A-Z0-9_]+)(;?)"),
                HelpStyles.TEXT_ENV_VAR,
            ),
            # -------------------------------------
            # [ 0] CMD_ARGUMENT
            # causes too many problems in cases where its not needed
            # self.RenderingRegexValRefilter(
            #     Regex(R"(?P<val>(?<![{@`´<])\b(?:[A-Z][A-Z0-9_]{3,})|END)(s?\b)"),
            #     FS(underlined=True),
            # ),
            # -------------------------------------
            # (-2) *WORD*
            self.RenderingValGroupRefilter(
                Regex(R"(^|)?\*(?P<val>[\w\u0302!/.-]+?)\*"),
                HelpStyles.TEXT_ACCENT,
            ),  # U+ 302 ▕  ̂ ▏ Mn COMBINING CIRCUMFLEX ACCENT
            # -------------------------------------
            # (**) 'es7s exec ls'
            self.LiteralReplacer(),
            # -------------------------------------
            # (-2) `dynamic result width example`
            #  =>  dynamic result width example    (result will be shorter by 2 chars)
            self.RenderingValGroupRefilter(
                Regex(Rf"`{self.WRAP_RE}(?P<val>.+?)`"),
                HelpStyles.TEXT_EXAMPLE,
            ),
            # -------------------------------------
            # [ 0] ´FIXED RESULT WIDTH EXAMPLE´
            #  =>  ␣FIXED RESULT WIDTH EXAMPLE␣  (post-markup-removing width compensation)
            pt.filter.StringReplacerChain(
                Regex(Rf"´.+?´"),
                self.RenderingValGroupRefilter(
                    Regex(Rf"´{self.WRAP_RE}(?P<val>.+?)´"),
                    HelpStyles.TEXT_EXAMPLE,
                ),
                pt.OmniPadder(),
            ),
            # -------------------------------------
            # (-2) <CONFIG_VAR>
            #  =>  CONFIG_VAR
            self.InlineConfigVarReplacer(import_from),
            # -------------------------------------
            # [ 0] {ENVIRONMENT_VAR}
            #  =>  ␣ENVIRONMENT_VAR␣
            pt.StringReplacerChain(
                Regex(Rf"(\{{){self.WRAP_RE}([\w.*-]+?)(}})"),
                pt.StringReplacer(Regex(R"\{(.+)}"), r" \1 "),
                self.RenderingValGroupRefilter(
                    Regex(R"(?P<val>.+)"),
                    HelpStyles.TEXT_ENV_VAR,
                ),
            ),
            # -------------------------------------
            # (-2) @ENVIRONMENT_VAR@
            #  =>  ENVIRONMENT_VAR
            self.RenderingValGroupRefilter(
                Regex(r"@(?P<val>[()\w._-]+?)@"),
                HelpStyles.TEXT_ENV_VAR,
            ),
            # -------------------------------------
            # (-4) ++dependency/format++
            #  =>  dependency/format
            self.RenderingValGroupRefilter(
                Regex(r"\+\+(?P<val>[\w./-]+?:*)\+\+"),
                HelpStyles.TEXT_DEPENDENCY,
            ),
            # -------------------------------------
            # (±0) ::LABEL::
            #       ▁▁▁▁▁▁▁
            #  ≈>  ␣▏LABEL▕␣
            #       ▔▔▔▔▔▔▔
            pt.StringReplacerChain(
                Regex(R"::(?P<val>[\w./-]+?:*)::"),
                pt.OmniPadder(2),
                self.RenderingNamedGroupsRefilter(
                    Regex(R"(?P<s1>\s)(\s)::(.+)::(\s)(?P<s2>\s)"),
                    {"": HelpStyles.TEXT_ABOMINATION},  # any
                ),
            ),
            # -------------------------------------
            # (-2)L //this is comment
            #  =>   this is comment
            self.RenderingValGroupRefilter(
                Regex(R"(^|\s+)//(?P<val>\s.+)"),
                HelpStyles.TEXT_COMMENT,
            ),
            # -------------------------------------
            # (-4) /*this is comment, too*/
            #  =>  this is comment, too
            self.RenderingValGroupRefilter(
                Regex(R"/\*(?P<val>.+?)\*/", dotall=True),
                HelpStyles.TEXT_COMMENT,
            ),
            # -------------------------------------
            # (±0) [[builtin]]
            #      ▁▁▁
            #  ≈>  ▏∙▕␣builtin
            #      ▔▔▔
            self.CommandTypeReplacer(),
            # -------------------------------------
            # (-2) <<placeholder>>
            #  =>  <placeholder>
            self.RenderingNamedGroupsRefilter(
                Regex(Rf"<(<){self.WRAP_RE}([\w\s.-]+?)(>)>"),
                {"": HelpStyles.TEXT_PLACEHOLDER},  # any
            ),
            # -------------------------------------
            # (-2) 'important'
            #  =>  important
            self.RenderingValGroupRefilter(
                Regex(Rf"(?<!\\)'{self.WRAP_RE}{self.OPTION_REGEX.pattern}'"),
                HelpStyles.TEXT_ACCENT,
            ),
            # -------------------------------------
            # (-2) ""important""
            #  =>  "important"
            pt.filter.StringReplacerChain(
                Regex(Rf'(?<!\\)""[^\x1b]+?""'),
                self.RenderingValGroupRefilter(
                    Regex(Rf'"{self.WRAP_RE}(?P<val>".+?")"'),
                    HelpStyles.TEXT_ACCENT,
                ),
                pt.StringReplacer(Regex(R'"'), R"\""),
            ),
            # -------------------------------------
            # [ 0] "important"
            #  =>  ␣important␣
            pt.filter.StringReplacerChain(
                Regex(Rf'(?<!\\)"[^\x1b]+?"'),
                self.RenderingValGroupRefilter(
                    Regex(Rf'"{self.WRAP_RE}(?P<val>.+?)"'),
                    HelpStyles.TEXT_ACCENT,
                ),
                pt.OmniPadder(),
            ),
            # -------------------------------------
            # (-2) “very-important”
            #  =>  very-important
            pt.filter.StringReplacerChain(
                Regex(R"“(.+?)”", dotall=True),
                self.RenderingNamedGroupsRefilter(
                    Regex(R"“(?P<val>.+?)”", dotall=True),
                    {"val": HelpStyles.TEXT_KEY_TERM},  # any
                ),
            ),
            # -------------------------------------
            # [ 0] ...text [default: 3 hours]
            self.RenderingValGroupRefilter(
                Regex(Rf"(default:){self.WRAP_RE}(?P<val>.+?)([];])"),
                HelpStyles.TEXT_OPTION_DEFAULT,
            ),
            # -------------------------------------
            # [ 0] ...text [which is a default]
            # self.RenderingRegexValRefilter(
            #     Regex(Rf"(\[)([\w\s]+)(?P<val>default)(])"),
            #     HelpStyles.TEXT_OPTION_DEFAULT,
            # ),
            # -------------------------------------
            # [ 0] ^ALTERNATIVE^
            #  =>  ␣ALTERNATIVE␣
            pt.filter.StringReplacerChain(
                Regex(Rf"\^.+?\^"),
                self.RenderingValGroupRefilter(
                    Regex(Rf"\^{self.WRAP_RE}(?P<val>.+?)\^"),
                    HelpStyles.TEXT_ALTER_MODE,
                ),
                pt.OmniPadder(),
            ),
            # -------------------------------------
            # [ 0] ░░░░░░░
            self.RenderingValGroupRefilter(
                Regex(R"(?P<val>░{2,})"),
                HelpStyles.TEXT_WALL,
            ),
            # -------------------------------------
            # (-1) &process ≈> Process
            # (-3) s&(ocks) ≈> sOCKS
            self.RenderingNamedGroupsRefilter(
                Regex(r"&(?:(?P<sval>\w)|\((?P<mval>\w+)\))"),
                {
                    "sval": HelpStyles.TEXT_ABBREV_SINGLE,
                    "mval": HelpStyles.TEXT_ABBREV_MULTI,
                },
            ),
            # -------------------------------------
            # (-1) it\'s => it's
            pt.StringReplacer(r"\\\'", "'"),
            # -------------------------------------
            # (-2) \"as is\" => "as is"
            pt.StringReplacer(r"\\\"", '"'),
            # -------------------------------------
            # [ 0] https://github.com
            self.RenderingNamedGroupsRefilter(
                URL_REGEX,
                {
                    "": HelpStyles.TEXT_URL,
                },
            ),
        ]

    def apply(self, string: str) -> str:
        return pt.apply_filters(string, *self._filters)


class HelpFormatter(click.HelpFormatter):
    command_names: ClassVar[list[str]]

    def __init__(self, width: int = None, max_width: int = None):
        ctx = click.get_current_context(True)
        width = pt.get_preferable_wrap_width(False)

        import_from = None
        if ctx and isinstance(ctx.command, CliCommand):
            import_from = ctx.command._import_from

        self._nwml = NWMarkup(import_from)
        super().__init__(2, width)

        if not hasattr(HelpFormatter, "command_names"):
            HelpFormatter.command_names = [APP_NAME]
            if ctx is None:
                return
            HelpFormatter.command_names = self._find_all_command_names(ctx.find_root().command)

    def _find_all_command_names(self, command: click.Command) -> set[str]:
        names = set()
        names.add(command.name)
        if hasattr(command, "commands") and isinstance(command.commands, dict):
            for nested_command in command.commands.values():
                names = names.union(self._find_all_command_names(nested_command))
        return names

    @classmethod
    @overload
    def format_command_name(cls, cmd: CliBaseCommand) -> str:
        ...

    @classmethod
    @overload
    def format_command_name(cls, name: re.Match | str) -> str:
        ...

    @classmethod
    def format_command_name(cls, arg) -> str:
        if isinstance(arg, CliBaseCommand):
            ct = arg.get_command_type()
            return get_stdout().render(arg.name, ct.get_name_fmt(arg.default_in_group))
        if isinstance(arg, re.Match):
            arg = arg.group(1)
        return get_stdout().render(arg, HelpStyles.TEXT_COMMAND_NAME)

    def format_accent(self, arg: re.Match | str) -> str:
        if isinstance(arg, re.Match):
            arg = arg.group(1) + arg.group(2)
        return get_stdout().render(arg, HelpStyles.TEXT_ACCENT)

    @contextmanager
    def section(self, name: str | None) -> t.Iterator[None]:
        # modified version of parent implementation; could not inject otherwise
        # changes: `name` is nullable now; do not write heading if `name` is empty
        self.write_paragraph()
        if name:
            self.write_heading(name)
        self.indent()
        try:
            yield
        finally:
            self.dedent()

    @classmethod
    def format_command_icon(cls, cmd: CliBaseCommand) -> pt.Fragment:
        ct = cmd.get_command_type()
        icon_char = ct.char
        icon_color = ct.get_icon_char_fmt(cmd.get_command_trait().fmt)
        return pt.Fragment(icon_char, icon_color)

    @classmethod
    def format_command_icon_and_name(cls, cmd: CliBaseCommand) -> pt.Text:
        return cls.format_command_icon(cmd) + " " + cls.format_command_name(cmd)

    @classmethod
    def format_command_attribute_legend(cls, ct: CommandAttribute) -> pt.Text:
        if isinstance(ct, CommandType):
            return (
                pt.Fragment("[")
                + pt.Fragment(ct.char, ct.get_icon_char_fmt())
                + pt.Fragment("] " + ct.name)
            )
        return pt.Fragment(f" {ct.char} ", ct.get_icon_char_fmt()) + pt.Fragment(" " + ct.name)

    @classmethod
    def format_command_type_inlined(cls, ct: CommandAttribute, icon_only=False) -> pt.RT:
        result: pt.RT = cls.format_command_own_type(ct)
        if not icon_only:
            result += pt.Fragment(" " + ct.name)
        return result

    @classmethod
    def format_command_own_type(cls, ct: CommandAttribute) -> pt.Fragment:
        return pt.Fragment(ct.get_own_char(), ct.get_own_fmt())

    def write_heading(
        self,
        heading: str,
        newline: bool = False,
        colon: bool = True,
        st: pt.Style = HelpStyles.TEXT_HEADING,
    ):
        # changes: styling of the header, optional newline
        heading = get_stdout().render(heading + (colon and ":" or ""), st)
        self.write(f"{'':>{self.current_indent}}{heading}")
        self.write_paragraph()
        if newline:
            self.write_paragraph()

    def write_text(self, text: str) -> None:
        # changes: sgr-aware wrapper, ⏺ list subseq indent handling
        is_list = text.lstrip().startswith(LIST_CHAR)
        indent_subseq_extra = (0, self.indent_increment)[is_list]
        self.write(
            pt.wrap_sgr(
                text,
                self.width,
                indent_first=self.current_indent,
                indent_subseq=self.current_indent + indent_subseq_extra,
            )
        )

    def write_squashed_text(self, string: str):
        wrapped_text = pt.wrap_sgr(
            string,
            self.width,
            indent_first=self.current_indent,
            indent_subseq=self.current_indent,
        )
        self.write(wrapped_text.replace("\n\n", "\n"))  # @REFACTOR wat
        self.write("\n")

    def write_dl(
        self,
        rows: t.Sequence[tuple[RT, RT]],
        col_max=30,
        col_spacing=2,
        dynamic_col_max=False,
    ):
        if dynamic_col_max:
            col_max = self.width // 2.5

        render = get_stdout().render
        add_markers = False
        rows_str = []
        for row in rows:
            if all(isinstance(cell, str) for cell in row):
                rows_str.append(row)
            else:
                add_markers = True
                rows_str.append((render(row[0]), render(row[1])))

        if add_markers:
            self.write(self._nwml.PROCESSED_SEGMENT_START)

        super().write_dl(rows_str, col_max, col_spacing)

        if add_markers:
            self.write(self._nwml.PROCESSED_SEGMENT_END)

    # def write(self, string: str) -> None:
    #     ...
    #     self.buffer.append(string)

    def _postprocess(self, string: str) -> str:
        if m := self._nwml.PROCESSED_SEGMENT_REGEX.search(string):
            return (
                self._postprocess(string[: m.span(0)[0]])
                + m.group(1)
                + self._postprocess(string[m.span(0)[1] :])
            )

        stripped = string.strip()
        if stripped in HelpFormatter.command_names:
            string = get_stdout().render(string, HelpStyles.TEXT_COMMAND_NAME)

        return self._nwml.apply(string)

    def getvalue(self) -> str:
        return self._postprocess(super().getvalue())


class Context(click.Context):
    formatter_class = HelpFormatter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed = False
        self.color = get_stdout().color
        self.logger_setup: LoggerSettings = get_logger().setup

    def fail(self, message: str):
        self.failed = True
        raise UsageError(message, ctx=self)


class UsageError(click.UsageError):
    def __init__(self, message: str, ctx: t.Optional[Context] = None) -> None:
        super().__init__(message, ctx)
        self.ctx = ctx

    def show(self, file: t.Optional[t.IO] = None) -> None:
        if not self.ctx.logger_setup.print_usage_errors:
            return
        super().show(file)


class CliBaseCommand(click.Command):
    context_class = Context

    def __init__(self, name, **kwargs):
        kwargs.setdefault("type", CMDTYPE_BUILTIN)
        self._include_common_options_epilog = kwargs.pop("include_common_options_epilog", True)
        self._include_common_options_interlog = kwargs.pop("_include_common_options_interlog", True)
        self._command_type: CommandType = kwargs.pop("type")
        self._command_traits: t.Sequence[CommandTrait] = self._resolve_traits(
            kwargs.pop("traits", [])
        )
        self._prolog = kwargs.pop("prolog", [])
        self._interlog = kwargs.pop("interlog", [])
        self._usage_override = kwargs.pop("usage_override", None)
        self._usage_section_name = kwargs.pop("usage_section_name", "Usage")
        self._default_in_group = False  # filled by autodiscover

        base_name = name or kwargs.get("name")
        if ".py" in base_name:
            base_name = splitext(basename(base_name))
            self._file_name_parts = base_name[0].lstrip("_").split("_")
        else:
            self._file_name_parts = [base_name]

        context_settings = kwargs.pop("context_settings", {})
        context_settings_extras = {
            "help_option_names": ["--help", "-?"],
            "ignore_unknown_options": kwargs.pop("ignore_unknown_options", None),
            "allow_extra_args": kwargs.pop("allow_extra_args", False),
        }
        context_settings.update(pt.filterfv(context_settings_extras))

        super().__init__(name, context_settings=context_settings, **kwargs)

    def get_command_type(self) -> CommandType:
        return self._command_type

    def get_command_trait(self) -> CommandTrait:
        if self._command_traits:
            return self._command_traits[-1]
        return CMDTRAIT_NONE

    def parse_args(self, ctx: Context, args: t.List[str]) -> t.List[str]:
        get_logger().debug(f"Pre-click args:  {format_attrs(args)}")
        try:
            return super().parse_args(ctx, args)
        except click.UsageError as e:
            ctx.fail(e.format_message())

    def invoke(self, ctx: Context) -> t.Any:
        get_logger().debug(f"Post-click args: {format_attrs(ctx.params)}")
        try:
            return super().invoke(ctx)
        except click.ClickException as e:
            ctx.failed = True
            self.show_error(ctx, e)

    def show_error(self, ctx: Context, e: click.ClickException):
        logger = get_logger()
        logger.error(e.format_message())
        if not logger.setup.print_click_errors:
            return

        hint = ""
        if ctx.command.get_help_option(ctx):
            hint = f"\nTry '{ctx.command_path} {ctx.help_option_names[0]}' for help."
        get_stdout().echo(f"{ctx.get_usage()}\n{hint}")

    def _resolve_traits(self, items: list[CommandTrait | str]) -> list[CommandTrait]:
        def __resolve(item: CommandTrait | str) -> CommandTrait | None:
            if isinstance(item, CommandTrait):
                return item
            if isinstance(item, str):
                return CommandTrait.get(item)
            return None

        def __iter() -> Iterable[CommandTrait]:
            for item in items:
                if (res := __resolve(item)) is not None:
                    yield res
                else:
                    get_logger(require=False).warning(f"Unresolvable trait: {item!r}")

        return [*__iter()]

    def _make_command_name(self, orig_name: str, with_group: bool = False) -> str:
        dir_name = basename(dirname(orig_name)).rstrip("_")  # 'exec_' -> 'exec'
        filename_parts = splitext(basename(orig_name))[0].rstrip("_").split("_")
        if filename_parts[0] == "":  # because of '_group' -> ['', 'group']
            filename_parts = [dir_name]
        result = "-".join(filename_parts)
        if with_group:
            return dir_name + "-" + result
        return result

    def _make_short_help(self, **kwargs) -> str:
        help_str = kwargs.get("help")
        if not help_str and not kwargs.get("prolog", None):
            get_logger(require=False).warning(f"Missing help for '{kwargs.get('name')}' command")
            help_str = "..."

        short_help = kwargs.get("short_help")
        short_help_auto = help_str.lower().removesuffix(".")
        if isinstance(short_help, t.Callable):
            return short_help(short_help_auto)
        elif short_help:
            return short_help
        return short_help_auto

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        usages: list[str]
        if self._usage_override:
            usages = [f"[OPTIONS] {usage}" for usage in self._usage_override]
        else:
            pieces = self.collect_usage_pieces(ctx)
            if self._command_type in [CMDTYPE_INTEGRATED, CMDTYPE_EXTERNAL]:
                pieces += ["[--", "PASSARGS]"]
            usages = [" ".join(pieces)]

        with formatter.section(self._usage_section_name):
            for usage in usages:
                formatter.write_usage(
                    formatter.format_command_name(ctx.command_path), usage, prefix=""
                )

    # def format_own_type(self, ctx: Context, formatter: HelpFormatter):
    #     stdout = get_stdout()
    #
    #     with formatter.indentation():
    #         descriptions = []
    #         for ct in [self.get_command_type(), self.get_command_trait()]:
    #             ct_icon = stdout.render(formatter.format_command_own_type(ct))
    #             ct_description = (
    #                 ct.description % ct_icon if "%s" in ct.description else ct.description
    #             )
    #
    #             if ct_description.count("|") == 2:
    #                 left, hightlight, right = ct_description.split("|", 2)
    #                 descriptions.append(
    #                     (
    #                         stdout.render(left, HelpStyles.TEXT_COMMENT)
    #                         + stdout.render(" " + hightlight + " ", ct.get_own_label_fmt())
    #                         + stdout.render(right, HelpStyles.TEXT_COMMENT)
    #                     )
    #                 )
    #             elif ct == CMDTYPE_INVALID:
    #                 descriptions.append(stdout.render(ct_description, ct.get_own_label_fmt()))
    #             else:
    #                 descriptions.append(ct_description)
    #
    #         formatter.write_paragraph()
    #         formatter.write_text("\n\n".join(filter(None, descriptions)))

    def format_common_options(self, ctx: Context, formatter: HelpFormatter, add_header: bool):
        if self._include_common_options_epilog:
            with formatter.section("Options" if add_header else ""):
                if add_header:
                    formatter.write_text("No specific options.")
                    formatter.write_paragraph()
                formatter.write_text(EPILOG_COMMON_OPTIONS.text)

    def format_prolog(self, ctx: Context, formatter: HelpFormatter) -> None:
        self._format_help_parts(formatter, [*self._get_help_parts(ctx, self._prolog)])

    def format_interlog(self, ctx: Context, formatter: HelpFormatter) -> None:
        self._format_help_parts(formatter, [*self._get_help_parts(ctx, self._interlog)])

    def format_epilog(self, ctx: Context, formatter: HelpFormatter) -> None:
        self._format_help_parts(formatter, [*self._get_help_parts(ctx, self.epilog)])

    def _get_help_parts(self, ctx: Context, src: t.Iterable[str | HelpPart]) -> t.Generator[list]:
        if src:
            if not pt.isiterable(src):
                src = [src]
            yield from src

    def _format_help_parts(self, formatter: HelpFormatter, parts: list[HelpPart]):
        squashed_parts = []
        for idx, part in enumerate(parts):
            if (
                len(squashed_parts)
                and not part.title
                and part.group
                and part.group == squashed_parts[-1].group
            ):
                squashed_parts[-1].text += "\n\n" + part.text
                continue
            squashed_parts.append(part)

        for part in squashed_parts:
            self._format_help_part(formatter, part)

    def _format_help_part(self, formatter: HelpFormatter, part: HelpPart):
        stdout = get_stdout()
        part_indent = part.indent_shift * formatter.indent_increment
        original_width = formatter.width
        formatter.current_indent += part_indent
        formatter.write_paragraph()
        if part.title:
            formatter.write_heading(part.title.capitalize(), newline=False, colon=False)
        if part.width_ratio:
            formatter.width = round(formatter.width * part.width_ratio)
        with formatter.indentation():
            if isinstance(part.text, str):
                formatter.write_text(part.text)
            elif pt.isiterable(part.text):
                formatter.write_dl(part.text)
            else:
                warn_frag = pt.Fragment(
                    f"WARNING: Invalid HelpPart text type: {type(part.text)}",
                    HelpStyles.WARNING,
                )
                formatter.write(stdout.render(warn_frag))
        formatter.current_indent -= part_indent
        formatter.width = original_width

    def _is_option_with_argument(self, option: click.Parameter) -> bool:
        if isinstance(option, ScopedOption):
            return option.has_argument()
        return False

    @property
    def default_in_group(self) -> bool:
        return self._default_in_group

    def set_default_in_group(self):
        self._default_in_group = True


class CliCommand(CliBaseCommand):
    """
    :param command_examples: list of strings/renderables. either of these
                             can contain '{}' which will be replaced with a
                             command full name. each item can also be
                             specified as a list of tuples which will be
                             formatted like a term-description list.
    :param output_examples:  same as for ``command_examples``.
    """

    option_scopes: list[OptionScope] = [
        OptionScope.COMMAND,
        OptionScope.GROUP,
    ]

    def __init__(
        self,
        import_from: str | None,
        command_examples: Iterable | None,
        output_examples: Iterable | None,
        **kwargs,
    ):
        name = kwargs.get("name")
        self._shared_opts = kwargs.pop("shared_opts", None)
        kwargs["name"] = self._make_command_name(name)

        kwargs.update(
            {
                "params": self._build_options(**kwargs),
                "short_help": self._make_short_help(**kwargs),
                "context_settings": {
                    "auto_envvar_prefix": "ES7S_" + self._make_command_name(name, with_group=True),
                },
            }
        )
        self._import_from = import_from
        self._command_examples = Section("Command examples", command_examples or [])
        self._output_examples = Section("Output examples", output_examples or [])
        self._ext_help_invoker: t.Callable[[Context], str] = kwargs.pop("ext_help_invoker", None)

        super().__init__(**kwargs)

    def _build_options(self, **kwargs) -> list[ScopedOption]:
        subclass_options = kwargs.get("params", [])
        all_options: list[ScopedOption] = [
            *subclass_options,
            *self._get_group_options(),
            *self._get_shared_options(),
        ]
        self._check_option_conflicts(all_options, **kwargs)
        return all_options

    def _check_option_conflicts(self, all_opts: list[ScopedOption], name: str, **kwargs):
        seen_opts = dict()
        for param in all_opts:
            for opt in param.opts:
                if opt not in seen_opts.keys():
                    seen_opts[opt] = param
                    continue
                conflict_msg = f"Option conflict in {name!r} for {opt!r}: "
                conflict_msg += ", ".join(f"({', '.join(p.opts)})" for p in [seen_opts[opt], param])
                get_logger(require=False).warning(conflict_msg)

    def _get_group_options(self) -> list[ScopedOption]:
        return []

    def _get_shared_options(self) -> list[ScopedOption]:
        if not self._shared_opts:
            return []

        def __iter():
            for shopt in self._shared_opts.items:
                yield from shopt

        return [*__iter()]

    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        self.format_usage(ctx, formatter)
        self.format_prolog(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_interlog(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)
        self.format_examples(ctx, formatter, self._command_examples)

        if self._ext_help_invoker is None:
            return
        result_generic = formatter.getvalue()
        formatter.buffer.clear()

        sep = f"{pt.ansi.SeqIndex.OVERLINED}{pt.pad(pt.get_terminal_width(pad=0))}{pt.ansi.SeqIndex.OVERLINED_OFF}"
        seq_color_bg = f"{pt.cv.GRAY_15.to_sgr(pt.ColorTarget.BG)}"
        seq_color_bg_line = f"{seq_color_bg}{pt.make_clear_line_after_cursor()}"

        inject_bg_rr = pt.StringReplacer(
            pt.SGR_SEQ_REGEX,
            lambda m: m.group(0) + (seq_color_bg if self._has_bg_or_reset_param(m) else ""),
        )
        enclose_bg_rr = pt.StringReplacer(compile("(^|\n|$)"), rf"\1{seq_color_bg_line}")
        result_generic = (
            pt.apply_filters(sep + "\n" + result_generic, inject_bg_rr, enclose_bg_rr)
            + pt.SeqIndex.RESET.assemble()
        )

        get_stdout().echo(result_generic)
        get_stdout().echo(sep)

        if result_component := self._ext_help_invoker(ctx):
            get_stdout().echo(result_component)
        else:
            formatter.write_heading(f"Component help")
            with formatter.indentation():
                formatter.write_text("<<Empty>>")
            get_stdout().echo(formatter.getvalue())
        formatter.buffer.clear()

    @staticmethod
    def _has_bg_or_reset_param(m: t.Match) -> bool:
        for c in m.group(3).split(";"):
            if not c:  # ""="0"
                return True
            try:
                i = int(c)
            except ValueError:
                continue
            if i in (pt.IntCode.RESET, pt.IntCode.BG_COLOR_OFF, pt.IntCode.INVERSED_OFF):
                return True

    def format_help_text(self, ctx: Context, formatter: HelpFormatter) -> None:
        super().format_help_text(ctx, formatter)
        self.format_examples(ctx, formatter, self._output_examples)
        # self.format_own_type(ctx, formatter)

    def format_options(self, ctx: Context, formatter: HelpFormatter):
        opt_scope_to_opt_help_map: dict[str, list[tuple[str, str]] | None] = {
            k: [] for k in OptionScope
        }
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None and hasattr(param, "scope"):
                opt_scope_to_opt_help_map[param.scope].append(rv)

        has_header = False
        for opt_scope in self.option_scopes:
            opt_helps = opt_scope_to_opt_help_map[opt_scope]
            if not opt_helps:
                continue
            if opt_scope.value:
                has_header = True
                with formatter.section(opt_scope.value):
                    formatter.write_dl(opt_helps)
            else:
                formatter.write_paragraph()
                with formatter.indentation():
                    formatter.write_dl(opt_helps)

        if any(self._is_option_with_argument(opt) for opt in ctx.command.params):
            formatter.write_paragraph()
            with formatter.indentation():
                formatter.write_text(inspect.cleandoc(EPILOG_ARGS_NOTE.text))

        self.format_common_options(ctx, formatter, not has_header)

    def format_examples(self, ctx: Context, formatter: HelpFormatter, examples: Section) -> None:
        if not examples:
            return
        cmdname = formatter.format_command_name(ctx.command_path)

        def _transform(ex: pt.RT | t.Iterable[pt.RT]) -> str | tuple[str]:
            if pt.isiterable(ex):
                return (*map(_transform, ex),)

            if not isinstance(ex, str):
                ex = pt.render(ex)
            ex = re.sub(
                r"(\s)" + NWMarkup.OPTION_REGEX.pattern,  # костыль; сам по себе OPTION_REGEX
                formatter.format_accent(r"\1\2"),  # матчит "-15" в "--date Nov-15"
                ex,
            )
            if "{}" in ex:
                ex = ex.format(*[cmdname] * ex.count("{}"))
            return ex

        def _write(ex: pt.RT):
            formatter.write_text(_transform(ex))

        with formatter.section(examples.title.capitalize()):
            if all(isinstance(exp, tuple) for exp in examples.content):
                formatter.write_dl((*map(_transform, examples.content),))
                return
            for ex in examples.content:
                if isinstance(ex, tuple) and len(ex) > 1:
                    _write(ex[0])
                    formatter.indent()
                    [_write(excq) for excq in ex[1:]]
                    formatter.dedent()
                elif isinstance(ex, str) or pt.is_rt(ex):
                    _write(ex)
                else:
                    raise ValueError(
                        f"Command example should be a string or a renderable or a tuple of them, got: {ex!r}"
                    )


class CliGroup(click.Group, CliBaseCommand):
    TEXT_COMMAND_MATCHED_PART = FrozenStyle(fg=pt.cv.HI_BLUE, underlined=True)
    TEXT_COMMAND_SUGGEST_1ST_CHR = FrozenStyle(fg=pt.cv.HI_RED, bold=True, underlined=False)
    TEXT_COMMAND_SUGGEST_OTHERS = HelpStyles.TEXT_COMMAND_NAME

    recursive_command_list = True
    command_list_header = "Commands"

    def __init__(self, **kwargs):
        self._filepath = kwargs.get("name")
        self._autodiscover_extras = kwargs.pop("autodiscover_extras", None)
        self._default_subcommand = kwargs.pop("default_subcommand", None)

        kwargs.update(
            {
                "name": self._make_command_name(self._filepath),
                "short_help": self._make_short_help(**kwargs),
                "allow_extra_args": True,
                "invoke_without_command": self._default_subcommand is not None,
            }
        )
        kwargs.setdefault("type", CMDTYPE_GROUP)

        super().__init__(**kwargs)
        self.autodiscover()

    def invoke(self, ctx: Context) -> t.Any:
        if self._default_subcommand and not ctx.protected_args:
            _, cmd, __ = self.resolve_command(ctx, [self._default_subcommand])
            ctx.invoke(cmd)
            return
        return super().invoke(ctx)

    def autodiscover(self):
        from .autodiscover import AutoDiscover, AutoDiscoverExtras

        AutoDiscover.run(
            self, self._filepath, t.cast(AutoDiscoverExtras, self._autodiscover_extras)
        )

    def format_help_text(self, ctx: Context, formatter: HelpFormatter) -> None:
        super().format_help_text(ctx, formatter)
        # self.format_own_type(ctx, formatter)

    def format_options(self, ctx: Context, formatter: HelpFormatter) -> None:
        # no options for groups
        self.format_commands(ctx, formatter)
        # self.format_subcommand_attributes(formatter)

    def format_subcommand_attributes(self, formatter: HelpFormatter):
        cts = [
            *filter(
                lambda ct: not ct.hidden,
                {*self.get_command_attributes()},
            )
        ]
        if not len(cts):
            return

        formatter.write_paragraph()
        with formatter.indentation():
            formatter.write_text(
                "   ".join(
                    get_stdout().render(formatter.format_command_attribute_legend(ct))
                    for ct in sorted(cts, key=lambda ct: ct.sorter)
                )
            )
        formatter.write_paragraph()

    def format_commands(self, ctx: Context, formatter: HelpFormatter) -> None:
        # modified version of parent implementation; could not inject otherwise
        commands = []
        for cmds in [*self.list_commands_recursive(ctx)]:
            if not pt.isiterable(cmds):
                cmds = [cmds]
            cmd = cmds[-1]
            if cmd is None:
                continue
            if cmd.hidden:
                continue
            commands.append((" ".join(c.name for c in cmds), cmds))

        if len(commands):
            # +2 for command type
            limit = formatter.width - 6 - max(2 + len(cmd[0]) for cmd in commands)

            rows = []
            for cmd_path, cmds in commands:
                cmd = cmds[-1]
                help = cmd.get_short_help_str(limit)
                cmd_icon = formatter.format_command_icon(cmd) + " "
                cmd_name = " ".join(formatter.format_command_name(c) for c in cmds)
                cmd_name_str = get_stdout().render(cmd_icon + cmd_name)
                rows.append((cmd_name_str, help))

            if rows:
                with formatter.section(self.command_list_header):
                    formatter.write_dl(rows, col_spacing=4)

    def list_commands_recursive(self, ctx, level=0) -> tuple[CliCommand, ...]:
        for cmdname in sorted(self.commands):
            cmd = self.get_command(ctx, cmdname)
            print_sub = isinstance(cmd, CliGroup) and self.recursive_command_list
            if not print_sub:  # or level == 0:
                yield (cmd,)
            if print_sub:
                subcommands = cmd.list_commands_recursive(ctx, level=level + 1)
                yield from ((cmd, *subcommand) for subcommand in subcommands)

    def add_commands(self, commands: Iterable[click.Command]):
        for cmd in commands:
            self.add_command(cmd)

    def get_commands(self) -> dict[str, CliBaseCommand]:
        return cast(dict[str, CliBaseCommand], self.commands)

    def get_command(self, ctx, cmd_name) -> CliBaseCommand | None:
        """
        When there is no exact match, search for commands that begin
        with the string the user has been typed, and return the matched
        command if it is the only one matching (e.g., 'es7s e' -> 'es7s exec').
        Otherwise print the closest by levenshtein distance command if no
        matches were found ('es7s ez' -> 'es7s exec'), or print all the partial
        matches if there are more than 1 of them ('es7s m' -> 'es7s manage',
        'es7s monitor').
        """
        rv = super().get_command(ctx, cmd_name)
        if rv is not None:
            return cast(CliBaseCommand, rv)

        matches = []
        lev_match, lev_match_dist = None, None
        for c in self.list_commands(ctx):
            if c.startswith(cmd_name):
                matches.append(c)
            ld = Levenshtein.distance(cmd_name, c)
            if not lev_match or ld <= lev_match_dist:
                lev_match, lev_match_dist = c, ld

        if not matches:
            get_logger().debug(f"No matches")
            lev_msg = ""
            if lev_match:
                get_logger().debug(f"Closest by lev. distance: {lev_match}")
                lev_msg = f"\n\nThe most similar command is:\n    {lev_match}"
            ctx.fail(f"No such command: '{cmd_name}'{lev_msg}")
            return None
        elif len(matches) == 1:
            get_logger().debug(f"Matched by prefix: {matches[0]}")
            return super().get_command(ctx, matches[0])
        # elif len(matches) > 1:

        stdout = get_stdout()

        def format_suggestions(m: t.Iterable[str]) -> str:
            suggs = [*map(lambda s: s.removeprefix(cmd_name), m)]
            same_chars_after = max(map(len, suggs))
            for i in range(same_chars_after):
                if any(len(s) <= i for s in suggs):
                    same_chars_after = i
                    break
                if len({*map(lambda s: s[i], suggs)}) > 1:  # unique characters at position <i>
                    same_chars_after = i + 1
                    break
            get_logger().debug(f"Shortest unique seq. length = {same_chars_after:d}")
            return ", ".join(map(lambda s: format_suggestion(s, same_chars_after), suggs))

        def format_suggestion(s: str, same_chars_after: int) -> str:
            return (
                stdout.render(cmd_name, self.TEXT_COMMAND_MATCHED_PART)
                + stdout.render(s[:same_chars_after], self.TEXT_COMMAND_SUGGEST_1ST_CHR)
                + stdout.render(s[same_chars_after:], self.TEXT_COMMAND_SUGGEST_OTHERS)
            )

        get_logger().debug(f"Several matches ({len(matches)}): {format_attrs(matches)}")
        ctx.fail(f"Several matches: {format_suggestions(sorted(matches))}")

    def resolve_command(self, ctx, args):
        # always return the full command name
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args

    def get_command_attributes(self, recursive: bool = False) -> t.Iterable[CommandAttribute]:
        for cmd in self.get_commands().values():
            if recursive and isinstance(cmd, CliGroup):
                yield from cmd.get_command_attributes(True)
            yield cmd.get_command_type()
            yield cmd.get_command_trait()

    def _get_help_parts(self, ctx: Context, src: t.Iterable[str | HelpPart]) -> t.Generator[list]:
        yield from super()._get_help_parts(ctx, src)
        yield EPILOG_COMMON_OPTIONS

        if not self.commands:
            return

        if non_group_subcmds := sorted(
            filter(lambda cmd: not isinstance(cmd, CliGroup), self.commands.values()),
            key=lambda v: v.name,
        ):
            example_cmd = non_group_subcmds[0]
        else:
            example_cmd = [*self.commands.values()][0]

        yield HelpPart(EPILOG_COMMANDS_TREE.text, group=EPILOG_COMMANDS_TREE.group)
        _, _, command_path = ctx.command_path.partition(" ")  # drop first 'es7s'
        if command_path.strip():
            command_path = " " + command_path
        yield HelpPart(
            EPILOG_COMMAND_HELP.text % (command_path, command_path, example_cmd.name),
            group=EPILOG_COMMAND_HELP.group,
        )

    @property
    def default_subcommand(self) -> str | None:
        return self._default_subcommand


def get_current_command_name() -> str:
    if ctx := click.get_current_context(True):
        if cmd := ctx.command:
            return cmd.name
    return "n/a"
