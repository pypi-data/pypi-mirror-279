#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core | endlessly (re)run a specified command, measure time and max memory
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
__SELF="$(basename "$0" | sed -Ee 's/\..+$//')"
__USAGE="$(cat <<-EOL
Endlessly run the specified COMMAND with ARGS, keep track of launch count and
latest exit code.

USAGE:
  ${__SELF} [-d DELAY] [--overlay] [--confirm] [COMMAND [ARGS...]]

OPTIONS:
  -d DELAY     Set waiting interval between runs to DELAY seconds, where DELAY is a floating-point number. Specify 0 to disable the waiting.
  --overlay    Do not clear terminal before each run
  --confirm    Require a key press after each run
EOL
)"
function :+ { sed <<<${*%;} -Ee 's/[^0-9:;]+/;/g; s/^.*$/\x1b[&m/;' | tr -d $'\n' ; }
function :- { :+ 0 ; }
function :: { :+ 0 "$@" ; }
# shellcheck disable=SC2046
__now() {  __fmtdate $(date "+%_e-%b %H : %M" ) ; }
__fmtdate() { printf "$(:+ 2)%s$(:+ 22 33) %s$(:+ 2)%s$(:+ 22)%s$(:+ 39)" "$@" ; }
__exit() { rm -f "$TMPFILE" ; printf "\x1b[2J\x1b[H" >&2 ; exit ; }
__main () {
    __pre_exec() {
      if [[ -z $ARG_OVERLAY ]] || [[ $restarts -eq 0 ]] ; then
          printf "\x1b[2J" >&2
      fi
      printf "\x1b[H" >&2
      [[ $excess -gt $(( -1 * (( totallen + ${#cmdlen} + 3 )) )) ]] && echo
    }
    __exec() {
        # ............................................................
        /usr/bin/time -o "$TMPFILE" -f $'\x1c%Es %MK \e[1;31m %x' "$@"
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    }
    __print_status() {
      local tstr="$(:: 90)-:--.--s ---K  -- "
      local rstr="-"
      local cmd="..."
      local now="-- ---  --:--"
      [[ $# -gt 1 ]] && {
        local tstr="$(grep -Ee $'^\x1c' -m1 "$TMPFILE" | sed -Ee 's/(\x1b\[[0-9;:]*)31([0-9;:]*m 0$)/\132\2/')"
        local rstr=$restarts ; [[ $restarts -gt 999 ]] && rstr=${restarts:0:-3}K
        local cmd="$(tr '\n' ' ' <<< "$*")"
        local now="$(__now)"
      }
      local totallen=$(( 14 + ${#cmd} + ${#rstr} + ${#tstr} + 4 - 8 ))
      local excess=$(( $totallen - $(tput cols) ))
      local cmdlen=$(( ${#cmd} - $excess ))
      local cmdstr=""; [[ $cmdlen -gt 0 ]] && cmdstr="${cmd:0:$cmdlen}"

      { # shellcheck disable=SC2059,SC2086
        printf "\e[H\e[9999G\e[${totallen}D" && \
        printf "$(:: 2 90)%s $(:: 1 34 48 5 17) %s $(:: 34 48 5 232) %s $(:-)" "$cmdstr" "$rstr" "$now" && \
        printf "$(:: 37) %s $(:-)" "$tstr"
      } | head -1 >&2  # atomic
    }

    trap __exit INT

    local restarts=0
    [[ $# -lt 1 ]] && set who #last -n$(($(tput lines)-5))

    touch "$TMPFILE"
    __pre_exec
    __exec true
    __print_status true

    while true ; do
        __exec "$@"

        [[ -n $ARG_CONFIRM ]] \
          && printf "Continue? (%s/%s): " "y" "$(:: 4)n$(::)" >&2 \
          && read -r -n1 yn >&2 \
          && case "$yn" in [Yy]*) ;; *) exit ;; esac

        __print_status "$@"

        [[ -n $ARG_DELAY ]] && sleep "$ARG_DELAY"
        ((restarts++))
    done
}

[[ $* =~ (--)?help ]] && echo "$__USAGE" && exit

declare TMPFILE=/tmp/sustain.$$.out
declare ARG_DELAY=1.0
declare ARG_OVERLAY=
declare ARG_CONFIRM=

while true ; do
  if [[ $1 == -d ]] ; then
      ARG_DELAY=$2 && shift 2
      [[ $ARG_DELAY =~ ^\s*0*\.0*\s*$ ]] && ARG_DELAY=
      continue
  fi
  [[ $1 == --overlay ]] && ARG_OVERLAY=true && shift && continue
  [[ $1 == --confirm ]] && ARG_CONFIRM=true && shift && continue
  break
done

__main "$@"
