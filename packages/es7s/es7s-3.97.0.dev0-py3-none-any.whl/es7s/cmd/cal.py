# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from datetime import datetime

from dateutil import rrule
from dateutil.rrule import WEEKLY

from ._base import _BaseAction
from ..shared import get_stdout


class action(_BaseAction):
    def __init__(self, *args, **kwargs):
        self._run(*args, **kwargs)

    def _run(self, dt: datetime, full: bool):
        rr = iter(rrule(freq=WEEKLY, dtstart=dt))

        stdout = get_stdout()
        stdout.echo(dt.strftime("%b %Y"))

        while True:
            wk = next(rr)
            if wk.month != dt.month:
                break
            print(wk)
            # dow = d.weekday()
            # if not cols[dow]:
            #     cols[dow] = [self._format_dow(d)]
            # cols[dow].append(f'{d.day:>2d}')

        # stdout.echo(' '.join(col.pop(0) for col in cols))
        # ptr = cols.index(min(*cols))
        # rr = iter(rrule(freq=WEEKLY, dtstart=dt))
        # for wk in rr:
        #     print(wk)

    def _format_dow(self, dt: datetime) -> str:
        return dt.strftime("%a")[:2]
