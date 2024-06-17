#!/usr/bin/bash
#//////////////////////////////////////////////////////////////////////////////
#////       /       /       /       /       /       /       /       /       ///
#///   P   /   R   /   O   /   T   /   O   /   T   /   Y   /   P   /   E   ////
#//       /       /       /       /       /       /       /       /       /////
#//////////////////////////////////////////////////////////////////////////////
# es7s/core
# (c) 2024 A. Shavykin <0.delameter@gmail.com>
#------------------------------------------------------------------------------
# read stdin, remove \e[*m seqs
deformat() { sed --unbuffered -Ee 's/─|▏|\x1b\[[0-9\;]*m//g; /^$/d';  }
#------------------------------------------------------------------------------

__main() {
  local f=cat
  [[ $* =~ -?-r(aw)? ]] && f=deformat
  __sub | $f
}

__sub() {
  grep -Ee 'CODM[^C]|CDM\s' -i <unicode_chart.txt |
#  grep -Ee 'U\+\s*E[5-9A-F]\S\S\s' -i <unicode_chart.txt |
    sed -Ee 's/.+(▕)\s*(\s\S+)\s*(▏).+/\x1b[38;5;20m\x1b[38;5;231;48;5;17m\2\x1b[;38;5;21m\3\x1b[m\t/;'  | __pp
  return
  grep -Ee 'comb' -i <unicode_chart.txt |
    sed -Ee 's/.+(▕)\s*(\s\S+)\s*(▏).+/\x1b[38;5;20m\x1b[38;5;231;48;5;17m\2\x1b[;38;5;21m\3\x1b[m\t/;'  | __pp

  grep -Ee 'latin' -i <unicode_chart.txt |
    sed -Ee 's/.+(▕)\s*(\S+)\s*(▏).+/\x1b[38;5;20m\x1b[38;5;231;48;5;17m\2\x1b[;38;5;21m\3\x1b[m\t/;'  | __pp

  grep -Ee 'full' -i <unicode_chart.txt |
    sed -Ee 's/.+(▕)\s*(\S+)\s*(▏).+/\x1b[38;5;20m\x1b[38;5;231;48;5;17m\2\x1b[;38;5;21m\x1b[m\t/;'  | __pp

  grep -Ee '10ff' -i <unicode_chart.txt |
    sed -Ee 's/.+(▕)\s*(\S+)\s*(▏).+/\x1b[38;5;20m\x1b[38;5;231;48;5;17m\2\x1b[;38;5;21m\3\x1b[m\t/;'  | __pp

  grep -Ee '1f[0-9A-F]{3}' -i <unicode_chart.txt |
    sed -Ee 's/.+(▕)\s*(\S+)\s*(▏).+/\x1b[38;5;20m\x1b[38;5;231;48;5;17m\2\x1b[;38;5;21m\3\x1b[m\t/;'  | __pp

  grep -Ee 'cyril' -i <unicode_chart.txt |
    sed -Ee 's/.+(▕)\s*(\S+)\s*(▏).+/\x1b[38;5;20m\x1b[38;5;231;48;5;17m\2\x1b[;38;5;21m\3\x1b[m\t/;'  | __pp

}

__pp() {
  sed -Ee '0~2s/48;5;17/48;5;18/g' |
    COLUMNS=$COLUMNS 7s -c column -g 0 -t 4 -s 1 -X |
    sed -Ee "/^$/s/^/\x1b[38;5;17m$(printf %$((COLUMNS - 1))s | tr ' ' @)\x1b[m/; s/@/─/g;"
}

set -e -o pipefail
unbuffer 7s -c groboc -w | head -n1   # tab stops at ×4
__main "$@"
