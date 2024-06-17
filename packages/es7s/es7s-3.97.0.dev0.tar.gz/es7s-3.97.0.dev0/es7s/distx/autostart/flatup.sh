#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2024 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
declare SELF=es7s/"${0##*/}"

__main() {
  if __update ; then
    __notify "flatpak apps updated"
  else
    __notify "flatpak apps failed to update"
  fi
}
__update() {
  flatpak update --noninteractive | __log
}
# shellcheck disable=SC2120
__log() {
  local level=${1:-info}
  logger --stderr --priority "local7.$level" --tag "${SELF}[$$]"
}
__notify() {
  local msg="${1:?}"
  notify-send -a "${SELF}" "${SELF}" "${msg}"
}

sleep 30
__main "$@"
