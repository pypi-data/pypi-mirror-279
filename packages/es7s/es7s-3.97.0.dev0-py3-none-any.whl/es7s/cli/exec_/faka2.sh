#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core | &(fak)e-&activity-v&2
# (c) 2024 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------

function _main() {
    local USAGE="$(cat <<-EOL
Usage:
    $(basename "$0")
EOL
    )"

    [[ $* =~ (--)?help ]] && { echo "$USAGE" ; exit ; }

    printf "\x1b[H\x1b[J"
    python -c 'import random,sys,time
MAG = 20
mag = MAG
mc = 1
TICK = 8e-3
prev = 0
interval = 0
polar = 0
a = 0
while True:
  time.sleep(TICK)

  interval =  (now := time.time_ns()) - prev
  prev = now
  if interval/1e9 > TICK * 1e3:
      mag = random.randint(MAG//2, MAG)
      mc = 5
  elif mc > 1:
      mc -= 1
  label = "OP"[polar > 0]
  sys.stderr.write(f"\x1b[0J\r \x1b[7m [{label}] \x1b[m {polar:5d}\x1b[m \x1b[7m INT \x1b[m {interval/1e6:4.1f}ms  \x1b[7m M \x1b[m {mag:-2d}x{mc:2d}")

  if abs(polar) < mc:
      polar = random.randint(1e3,3e3) * random.randint(-1,3)
  else:
      polar -= mc*(polar//abs(polar))

  if polar > 0:
      if mc > 1:
          a = random.randint(0, 360)
          r = random.randint(0, 2*mag*mc)
      else:
          a = (a + 5 * [-1, 1][(polar // 777) % 2]) % 360
          r = 20 - ((polar % (347)) // 20)
      sys.stderr.write(f" \x1b[7m A,R \x1b[m {a:4d} {r:4d}")
      sys.stderr.flush()
      sys.stdout.write(f"mousemove_relative --polar %d %d --sync sleep %.0e\n" % (a, r, TICK))
  else:
      x = random.randint(-mag*mc, mag*mc)
      y = random.randint(-mag*mc, mag*mc)
      sys.stderr.write(f" \x1b[7m X,Y \x1b[m {x:4d} {y:4d}")
      sys.stderr.flush()
      sys.stdout.write(f"mousemove_relative --sync -- %d %d sleep %.0e\n" % (x, y, TICK))

  sys.stderr.write(f"  \x1b[31;5mSTALE\x1b[m ")
  sys.stderr.flush()
  sys.stdout.flush()
  sys.stderr.write(f"\b"*6+" "*6)
  sys.stderr.flush()

    ' | es7s exec xdotool - -L
}

_main "$@"
