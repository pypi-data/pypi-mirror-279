# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import typing as t
from collections.abc import Iterable, Generator
from dataclasses import is_dataclass

import pytermor as pt
from pytermor import get_qname


def inspect(o: object, max_level: int = None, max_generator_items: int = 100, public_only: bool = True):
    prev_level = 0
    setattr(_traverse, "max_level", max_level)
    setattr(_traverse, "max_generator_items", max_generator_items)
    setattr(_traverse, "public_only", public_only)
    try:
        for args in _traverse(None, o):
            k, v, prim, level, acc, descent, visited, more = args
            # already_visited = level < 0
            if level < 0:
                level *= -1
            if prev_level > level and level < 1:
                print("")
            prev_level = level
            base = pt.Style()

            id_fg = pt.NOOP_COLOR
            if prim or v is None:
                id_fg = pt.cv.GRAY_30
            elif visited:
                base.fg = pt.cv.GRAY_50
                base.bg = pt.cv.GRAY_15
                id_fg = pt.cv.YELLOW

            id_st = pt.Style(base, fg=id_fg)
            idstr = pt.Fragment(" ".join(["".join(c) for c in pt.chunk(f"{id(v):012x}", 4)]), id_st)

            pad_st = pt.Style(base, crosslined=False)
            if level > 0:
                pad = pt.Fragment(" " + ("│  " * max(0, level - 1)) + "├─", pad_st)
            else:
                pad = ""
            # ─├

            key_st = pt.Style(base, crosslined=False)
            key_str = ""
            key_str_extra = " "
            if k is None and level == 0:
                key_st.fg = pt.NOOP_COLOR
                key_str = "⏺"  # "⬤" "⏺"
            else:
                key_str_extra = ": "
                if acc == property:
                    key_st.fg = pt.cv.MAGENTA
                elif isinstance(k, str):
                    key_st.fg = pt.cv.GREEN
                elif isinstance(k, (bytes, bytearray)):
                    key_st.fg = pt.cvr.PEAR
                elif isinstance(k, int):
                    key_st.fg = pt.cv.HI_BLUE
                key_str = str(k)
                if (key_repr := repr(k)).strip("'") != key_str:
                    key_str = key_repr
                if v.__class__.__name__ == "method":
                    key_st.fg = pt.cv.HI_YELLOW
                    key_str_extra = "()" + key_str_extra

            type_st = pt.Style(base, fg=pt.cv.GRAY, italic=True, crosslined=False)
            try:
                qname = get_qname(v)
            except Exception:
                qname = str(v)
            type_str = pt.Fragment(
                pt.fit(qname + " ", 30 - len(key_str + key_str_extra + pad)), type_st
            )

            if more:
                key_str = ""
                key_str_extra = '...'
                type_str = ""

            key_frag = pt.Fragment(key_str, pt.Style(key_st, bold=False))

            if prim:
                val_col = pt.cv.BLUE
                if isinstance(v, bool):
                    val_col = pt.cv.YELLOW
                if isinstance(v, str):
                    val_col = pt.cv.GREEN
                if isinstance(v, (bytes, bytearray)):
                    val_col = pt.cvr.PEAR
                if isinstance(v, type):
                    val_col = pt.cv.RED
                val_st = pt.Style(base, fg=val_col)
                val_frag = pt.Fragment(f"{v!r}", val_st)
            elif isinstance(v, t.Sized):
                len_brace_st = pt.Style(base, fg=pt.cv.GRAY)
                val_frag = pt.Composite(
                    pt.Fragment("(", len_brace_st),
                    pt.Fragment(str(len(v)), pt.Style(base, fg=pt.cv.CYAN, bold=True)),
                    pt.Fragment(")", len_brace_st),
                )
            elif v is None:
                val_frag = pt.Fragment("None", pt.Style(base, fg=pt.cv.GRAY))
            else:
                val_frag = pt.Fragment(repr(v), pt.Style(base))

            if more:
                val_frag = ""

            pt.echo(
                pt.Text(
                    idstr, pad, (" ", base), key_frag, (key_str_extra, base), type_str, val_frag, width=pt.get_terminal_width()
                )
            )
    finally:
        delattr(_traverse, "max_level")
        delattr(_traverse, "max_generator_items")
        delattr(_traverse, "public_only")
        delattr(_traverse, "visited")


def _traverse(k: any, o: object, _level=0, *, _accessor=None, _descent=True, _visited=0, _more=False):
    if not hasattr(_traverse, "visited"):
        _traverse.visited = dict()

    if o.__class__.__name__ == "builtin_function_or_method":
        return
    if max_level := getattr(_traverse, "max_level"):
        if _level > max_level:
            return
    if k and str(k).startswith('_') and getattr(_traverse, "public_only"):
        return

    is_primitive = isinstance(o, (str, int, float, bool, type, bytes, bytearray))
    oaddr = id(o)
    yield k, o, is_primitive, _level, _accessor, True, _traverse.visited.get(oaddr), _more

    if isinstance(_traverse.visited.get(oaddr), int):  # @REFACtOR THIS SHT
        _traverse.visited[oaddr] += 1
        return
    try:
        _traverse.visited[oaddr] = 1
    except TypeError:
        pass

    if isinstance(o, t.Mapping):
        mapkeys = [*o.keys()]
        for kk in mapkeys:
            yield from _traverse(kk, o.get(kk), _level + 1, _accessor=dict)
    # elif is_dataclass(o):
    #     for kk, vv in asdict(o).items():
    #         yield from _traverse(kk, vv, _level + 1, _accessor=dict)
    #     _descent = False
    elif isinstance(o, Iterable) and not isinstance(o, (str, bytes, bytearray)):
        for kk, vv in enumerate(o):
            more = isinstance(o, Generator) and kk >= getattr(_traverse, "max_generator_items")
            yield from _traverse(kk, vv, _level + 1, _accessor=list, _more=more)
            if more:
                break

    if is_primitive or not _descent:
        return
    for attr in dir(o):
        if attr.startswith("__"):
            continue
        try:
            nxt = getattr(o, attr)
        except Exception:
            continue
        yield from _traverse(attr, nxt, _level + 1, _accessor=property, _descent=is_dataclass(nxt))  # костыли-костылики %(
