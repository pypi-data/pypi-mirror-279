#!/bin/bash
set -ue
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2024 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
.f() { printf "\e[%sm" "$(tr -s ' ' \; <<<"$*")"; }
.r() { .f 0 ; }
__call() {
  __fmtcmd "$@"

  local retcode=0
  if "$@" ; then : ; else
    retcode=$?
    echo "Command failed with code $retcode"
    return $retcode
  fi
}
__fmtcmd() {
  local cmd="$1" fcmd=$(.f 94)
  shift
  printf "${fcmd}$(.f 1)>$(.r) ${fcmd}%s$(.r) $(.f 34)%s$(.r)\n" "$cmd" "$*"
}
# ---------------------------------------------------------
__main() {
  local src_dir="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
  local dst_dir="$HOME/.config/autostart"
  for src_file in "$src_dir"/* ; do
    local filename=$(basename "$src_file")
    if [[ $src_file =~ install.sh$ ]] || [[ ! -x "$src_file" ]] ; then
      continue
    fi
    local dst_file="${dst_dir%%/}/${filename%%.*}"
    #__call cp -uv "$src_file" "$dst_file"
    __call ln -vs "$src_file" "$dst_file"
#    __call chmod +x "$dst_file"
  done
}

__main "$@"
