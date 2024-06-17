#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2024 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
__SELF="$(basename "$0" | sed -Ee 's/\..+$//')"
__USAGE="$(cat <<-EOL
Convert terminal snapshot from xterm SVG -> PNG, replacing the font and colors.
Default font is "Iose7ka Terminal".

Usage:
    ${__SELF} SVG_FILE [FONT_NAME]
EOL
)"

__usage() { echo "$__USAGE" ; exit "${1:-0}" ; }
  __die() { echo "$@" ; exit 1; }
 __main() {
    local -r infile="$(realpath "$1")"
    local -r fontname="${2:-Iose7ka Terminal}"

    [[ -f "$infile" ]] || __die "ERROR: Not found: ${infile@Q}"
    if ! file "$infile" | grep XML
      then __die "ERROR: not an XML file: ${infile@Q}"
    fi

    sed -Ee "s/(font-family=)(.).+\2/\1\2$fontname\2/1" "$infile" -ibak
}

echo $PWD
[[ $* =~ (--)?help ]]      && __usage
[[ $# -lt 1 || $# -gt 2 ]] && __usage 2
__main "$@"
