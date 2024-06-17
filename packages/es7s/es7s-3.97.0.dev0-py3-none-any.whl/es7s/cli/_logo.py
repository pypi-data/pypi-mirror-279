from __future__ import annotations

import re

import pytermor as pt

from es7s import APP_VERSION
from es7s.shared import (
    FrozenStyle,
    get_stdout,
)


class LogoFormatter(pt.StringReplacer):
    B = "╲"
    F = "╱"
    REGEX = re.compile(
        rf"""
        (?P<ovmarks> \^+)
        |
        (
           (?P<accleft> {B+B+B})
           |
           (?P<acc> {F}{B}|{B}{F})
        )
        (?P<default>
          {B}+({F}+(?!{B}))?
          |
          {F}+(?!{B})
        )?
    """,
        flags=re.VERBOSE,
    )

    ST_ACCENT = FrozenStyle(fg=pt.cv.YELLOW)
    ST_DEFAULT = FrozenStyle(fg=pt.cv.BLUE)
    ST_ACCENT_OV = FrozenStyle(ST_ACCENT, overlined=True)
    ST_DEFAULT_OV = FrozenStyle(ST_DEFAULT, overlined=True)
    ST_SHADOW_OV = FrozenStyle(ST_DEFAULT_OV, dim=True)
    ST_VERSION = FrozenStyle(bold=True, dim=True)

    def __init__(self):
        super().__init__(self.REGEX, self.replace)

    def replace(self, m: re.Match) -> str:
        result = pt.Text()

        if group_overline_marks := m.group("ovmarks"):
            result += (" " * len(group_overline_marks), self.ST_SHADOW_OV)

        if group_accent_left := m.group("accleft"):
            result += (group_accent_left, self.ST_ACCENT)

        if group_accent := m.group("acc"):
            if group_accent.endswith(self.B):
                result += (group_accent[0], self.ST_ACCENT)
                result += (group_accent[1:], self.ST_ACCENT_OV)
            else:
                result += (group_accent, self.ST_ACCENT)

        if group_default := m.group("default"):
            if group_default.endswith(self.B):
                result += (group_default[:-1], self.ST_DEFAULT_OV)
                result += (group_default[-1], self.ST_DEFAULT)
            else:
                result += (group_default, self.ST_DEFAULT_OV)

        return get_stdout().render(result)

    @classmethod
    def render(cls) -> str:
        version_main, sep, version_sub = APP_VERSION.rpartition(".")
        version_sub = (sep + version_sub if version_sub else "").ljust(13 - len(version_main))
        version_str = get_stdout().render(
            pt.Text(
                ("v", pt.merge_styles(cls.ST_ACCENT_OV, overwrites=[cls.ST_VERSION])),
                (version_main, pt.merge_styles(cls.ST_SHADOW_OV, overwrites=[cls.ST_VERSION])),
                (version_sub, cls.ST_SHADOW_OV),
            )
        )

        s = rf"""
                                                                             
 ╱╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲     ╱╲╲╲╲╲╲╲╲╲╲╲    ╱╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲   ╱╲╲╲╲╲╲╲╲╲╲╲        
 ╲╲╲╲╲╱╱╱╱╱╱╱╱╱╱╱    ╱╲╲╲╱╱╱╱╱╱╱╱╱╲╲╲ ╲╱╱╱╱╱╱╱╱╱╱╱╱╱╲╲╲ ╱╲╲╲╱╱╱╱╱╱╱╱╱╲╲╲     
  ╲╲╲╲╲^^^^^^^^^     ╲╱╱╲╲╲╲^^^^^╲╱╱╱  ^^^^^^^^^^^╱╲╲╲╱ ╲╱╱╲╲╲╲^^^^^╲╱╱╱     
   ╲╲╲╲╲╲╲╲╲╲╲╲╲      ^╲╱╱╱╱╲╲╲╲  ^^             ╱╲╲╲╱   ^╲╱╱╱╱╲╲╲╲  ^^      
    ╲╲╲╲╲╱╱╱╱╱╱╱        ^^^╲╱╱╱╱╲╲╲╲            ╱╲╲╲╱      ^^^╲╱╱╱╱╲╲╲╲      
     ╲╲╲╲╲^^^^^             ^^^╲╱╱╱╱╲╲╲        ╱╲╲╲╱           ^^^╲╱╱╱╱╲╲╲   
      ╲╲╲╲╲              ╱╲╲╲   ^^^╲╱╱╲╲╲     ╱╲╲╲╱         ╱╲╲╲   ^^^╲╱╱╲╲╲ 
       ╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲ ╲╱╱╱╲╲╲╲╲╲╲╲╲╲╲╱    ╱╲╲╲╱          ╲╱╱╱╲╲╲╲╲╲╲╲╲╲╲╱ 
        ╲╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱  ^^╲╱╱╱╱╱╱╱╱╱╱╱     ╲╱╱╱            ^^╲╱╱╱╱╱╱╱╱╱╱╱  
         {version_str }      ^^^^^^^^^^       ^^                ^^^^^^^^^^   """

        def iter():
            inst = cls()
            for line in s.splitlines():
                yield pt.apply_filters(line, inst)
            yield ""

        return "\n".join(iter())
